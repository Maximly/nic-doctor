# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
"""Evidence-based NIC checks and conservative topology-aware IRQ placement."""


def relevant_devices(system, requested=None, include_all=False):
    if requested:
        system.device(requested)
        return [requested]
    names = system.devices()
    if include_all:
        return names
    physical = [dev for dev in names if dev != 'lo' and system.if_info(dev).get('pci')]
    return physical if physical else [dev for dev in names if dev != 'lo']


def finding(dev, code, severity, title, evidence, explanation, recommendation, confidence='high'):
    return {'device':dev, 'code':code, 'severity':severity, 'title':title,
            'evidence':evidence, 'explanation':explanation,
            'recommendation':recommendation, 'confidence':confidence}


def as_cpu_set(spec):
    try:
        return set(parse_cpulist(spec)) if spec else set()
    except DoctorError:
        return set()


def physical_key(topology, cpu):
    entry = topology.get(str(cpu), {})
    if entry.get('socket') is None or entry.get('core') is None:
        return None
    return (entry['socket'], entry['core'])


def queue_irqs(items):
    return [x for x in items if x['channel_index_hint'] is not None and x['pci_member']]


def numeric_link(speed):
    m = re.match(r'^\s*(\d+(?:\.\d+)?)\s+GT/s', str(speed))
    return float(m.group(1)) if m else None


def traffic_rates(deltas, elapsed, preference='auto'):
    """Select one accounting domain per direction, never sum overlapping domains."""
    if preference not in ('auto', 'phy', 'vport', 'netdev'):
        raise DoctorError('invalid traffic counter source')
    result = {}
    for direction in ('rx', 'tx'):
        sources = {
            'phy': ('PHY (port)', f'ethtool/{direction}_packets_phy', f'ethtool/{direction}_bytes_phy'),
            'netdev': ('netdev (host)', f'{direction}_packets', f'{direction}_bytes'),
        }
        vp = f'ethtool/{direction}_vport_'
        kinds = ('unicast', 'multicast', 'broadcast')
        vport_packets = [vp + kind + '_packets' for kind in kinds]
        vport_bytes = [vp + kind + '_bytes' for kind in kinds]
        if all(k in deltas for k in vport_packets + vport_bytes):
            sources['vport'] = ('vPort (PF)', sum(deltas[k] for k in vport_packets),
                                sum(deltas[k] for k in vport_bytes))
        chosen = None
        sequence = ('phy', 'vport', 'netdev') if preference == 'auto' else (preference,)
        for name in sequence:
            if name not in sources:
                continue
            label, packets_key, bytes_key = sources[name]
            packets = deltas.get(packets_key) if isinstance(packets_key, str) else packets_key
            bytes_ = deltas.get(bytes_key) if isinstance(bytes_key, str) else bytes_key
            if packets is not None or bytes_ is not None:
                chosen = (label, packets, bytes_)
                break
        label, packets, bytes_ = chosen if chosen else (None, None, None)
        result[direction + '_source'] = label
        result[direction + '_pps'] = packets / elapsed if packets is not None and elapsed > 0 else None
        result[direction + '_bps'] = bytes_ * 8 / elapsed if bytes_ is not None and elapsed > 0 else None
        result[direction + '_mpps'] = round(result[direction + '_pps'] / 1e6, 6) if result[direction + '_pps'] is not None else None
        result[direction + '_gbps'] = round(result[direction + '_bps'] / 1e9, 6) if result[direction + '_bps'] is not None else None
    return result


def human_rate(value, suffix):
    if value is None:
        return '-'
    for size, prefix in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k')):
        if value >= size:
            return f'{value / size:.3f} {prefix}{suffix}'
    return f'{value:.2f} {suffix}'


def collect_state(system, devices, sample_seconds=0, vendors=False, traffic_source='auto'):
    if not (0 <= sample_seconds <= 300):
        raise DoctorError('sample duration must be within 0..300 seconds')
    state = {}
    for dev in devices:
        info = system.if_info(dev)
        state[dev] = {'info':info, 'irqs':system.iface_irqs(dev), 'rss':system.rss(dev),
                      'counters_before':system.counters(dev, vendors)}
    elapsed = 0.0
    if sample_seconds > 0:
        before = time.monotonic()
        time.sleep(sample_seconds)
        for dev in devices:
            state[dev]['counters_after'] = system.counters(dev, vendors)
        elapsed = time.monotonic()-before
    else:
        for dev in devices:
            state[dev]['counters_after'] = state[dev]['counters_before']
    for dev in devices:
        item = state[dev]
        start, end = item['counters_before'], item['counters_after']
        item['counter_deltas'] = {k:end[k]-v for k,v in start.items()
                                  if k in end and end[k] >= v}
        item['reset_counters'] = sorted(k for k,v in start.items() if k in end and end[k]<v)
        item['rates'] = traffic_rates(item['counter_deltas'], elapsed, traffic_source)
    return state, elapsed


def analyze_device(system, dev, item, elapsed, focus='all'):
    info, irqs, rss, deltas = item['info'], item['irqs'], item['rss'], item['counter_deltas']
    out=[]
    def add(code, category, severity, title, evidence, explanation, recommendation, confidence='high'):
        if focus in ('all',category):
            out.append(finding(dev,code,severity,title,evidence,explanation,recommendation,confidence))

    if info.get('pci') and info.get('operstate') in ('down','lowerlayerdown'):
        add('link.down','link','info','Link is not operational',
            f'operstate={info["operstate"]} (sysfs)',
            'The interface may be administratively disabled or its physical link may be down.',
            'Inspect administrative state, carrier and peer link; no automatic change is proposed.', 'medium')

    if info.get('pci_chain'):
        endpoint=info['pci_chain'][-1]
        cur_speed=numeric_link(endpoint.get('pcie_link_speed'))
        max_speed=numeric_link(endpoint.get('pcie_max_speed'))
        try:
            width=int(endpoint.get('pcie_link_width'))
            maximum=int(endpoint.get('pcie_max_width'))
        except (ValueError,TypeError):
            width=maximum=None
        if (cur_speed and max_speed and cur_speed+0.01<max_speed) or (width and maximum and width < maximum):
            add('pcie.below_capability','pcie','warning','PCIe link negotiated below endpoint capability',
                f'{pci_link(endpoint)} (sysfs; endpoint {endpoint["pci"]})',
                'The link may be constrained by the slot, upstream device or firmware. This is not proof of a throughput bottleneck.',
                'Check slot wiring, BIOS PCIe settings and upstream negotiated links.', 'high')

    combined=((info.get('channels') or {}).get('current') or {}).get('combined')
    if rss is not None and combined:
        invalid=sorted(set(q for q in rss if q >= combined))
        if invalid:
            add('rss.outside_channels','rss','warning','RSS table references channels outside the current range',
                f'RSS queues {invalid}; combined channels={combined} (ethtool -x/-l)',
                'The indirection table and channel configuration appear inconsistent.',
                f'Inspect RSS and channel layout: nic-doctor rss {dev}.', 'medium')
        counts={q:rss.count(q) for q in set(rss)}
        if len(counts)>1 and min(counts.values())>0 and max(counts.values())>2*min(counts.values()):
            add('rss.uneven_weights','rss','info','Uneven RSS indirection weights',
                f'queue slot counts={dict(sorted(counts.items()))} (ethtool -x)',
                'Indirection weights are unequal; this does not show actual packet or flow imbalance.',
                'Check per-queue packet deltas before considering an RSS rebalance.', 'high')
    elif rss is None:
        add('rss.unavailable','rss','info','RSS mapping unavailable',
            f'ethtool RSS indirection could not be read for {dev}',
            'RSS may be unsupported or unavailable to this account/driver.',
            'Inspect driver capabilities before trying RSS configuration.', 'high')

    local=set()
    if info.get('numa_node') not in (None,'-1'):
        local=set(system.numa_cpus(info['numa_node']))
    labelled=queue_irqs(irqs)
    if local:
        remote=[x for x in labelled if (as_cpu_set(x.get('effective_affinity')) and
                 as_cpu_set(x['effective_affinity']).isdisjoint(local))]
        if remote:
            add('irq.remote_numa','placement','warning','Completion IRQs are outside NIC-local NUMA node',
                f'{len(remote)} channel-labelled PCI IRQs remote: '+', '.join(str(x['irq']) for x in remote[:12])+
                f'; NUMA node={info["numa_node"]} (sysfs, procfs)',
                'Remote interrupt handling can increase latency and cross-NUMA activity; performance impact must be measured.',
                f'Inspect CPU placement: nic-doctor optimize {dev}.', 'high')

        single=[(x,next(iter(as_cpu_set(x['effective_affinity'])))) for x in labelled
                if len(as_cpu_set(x.get('effective_affinity')))==1]
        topology=system.cpu_topology(sorted({cpu for _,cpu in single}|local))
        by_core={}
        for x,cpu in single:
            core=physical_key(topology,cpu)
            if core is not None:
                by_core.setdefault(core,[]).append(x['irq'])
        clashes={core:ids for core,ids in by_core.items() if len(ids)>1}
        freecores={physical_key(topology,c) for c in local if physical_key(topology,c) is not None}-set(by_core)
        if clashes and freecores:
            add('irq.shared_core','placement','warning','Completion IRQs share physical cores',
                f'{len(clashes)} physical core(s) have multiple labelled IRQs while {len(freecores)} local cores are unused',
                'Distinct IRQ affinities on SMT siblings can contend for the same execution resources; this is a tuning opportunity, not proven loss.',
                f'Preview a core-aware mapping: nic-doctor optimize {dev}.', 'medium')
    if not labelled:
        add('irq.mapping_unknown','placement','info','Completion IRQ mapping not established',
            f'{len(irqs)} PCI/name-attributed IRQs; 0 verified PCI-member channel labels',
            'MSI-X vector order does not prove queue/NAPI correspondence.',
            'Inspect nic-doctor cpu-map; pinning needs explicit unambiguous channel labels.', 'high')

    if elapsed > 0:
        scope = []
        for direction in ('rx', 'tx'):
            physical = deltas.get(f'ethtool/{direction}_packets_phy', 0)
            netdev = deltas.get(f'{direction}_packets')
            if physical > 0 and netdev == 0:
                scope.append(f'{direction.upper()}: physical +{physical}, netdev +0')
        if scope:
            add('traffic.accounting_domains', 'loss', 'info',
                'Physical-port traffic absent from netdev counters',
                '; '.join(scope),
                'Physical NIC counters include traffic that Linux interface statistics may omit, including XDP processing. This does not establish packet loss.',
                'Compare physical-port, vPort, and XDP action counters before interpreting traffic volume.', 'high')
        # Names are driver-specific; never sum per-port/PF/queue counters together.
        signals=[('ethtool/rx_out_of_buffer','rx.out_of_buffer','RX buffer exhaustion counter increased',
                  'A NIC/driver RX resource counter increased during sampling; its exact counter scope is driver-specific.',
                  'Inspect RX rings, queue servicing, burst behavior and vendor counter definitions.'),
                 ('ethtool/rx_buff_alloc_err','rx.alloc_error','RX buffer allocation errors increased',
                  'Driver allocation failures may impair RX replenishment.',
                  'Inspect memory pressure and driver allocation behavior.'),
                 ('rx_missed_errors','rx.missed','RX missed packets increased',
                  'The standard missed-packet counter increased; underlying drop stage is device-specific.',
                  'Inspect driver/NIC queue pressure and packet bursts.'),
                 ('rx_dropped','rx.dropped','RX dropped counter increased',
                  'The Linux RX dropped counter increased; it may count software or device-specific conditions.',
                  'Inspect drop accounting and local kernel/driver path.'),
                 ('tx_dropped','tx.dropped','TX dropped counter increased',
                  'The Linux TX dropped counter increased.',
                  'Inspect TX queues, qdiscs and driver counters.')]
        for key,code,title,reason,next_step in signals:
            change=deltas.get(key,0)
            if change>0:
                add(code,'loss','warning',title,
                    f'{key}: +{change} over {elapsed:.2f}s ({key.split("/")[0]} counters)',
                    reason,next_step, 'high')
        # Additional vendor error names are distinct signals; report only a few to limit noise.
        covered={x[0] for x in signals}
        other=sorted(((key,val) for key,val in deltas.items()
                      if key.startswith('ethtool/') and key not in covered and val>0 and DROP_RE.search(key)),
                     key=lambda pair:-pair[1])[:5]
        if other:
            add('driver.additional_errors','loss','info','Additional vendor drop/error counters increased',
                ', '.join(f'{key}: +{val}' for key,val in other),
                'The meanings and scopes of these driver-defined counters differ; some may overlap with standard counters.',
                'Consult the driver counter definitions and compare with physical-port counters.', 'medium')
        if item['reset_counters']:
            add('counter.reset','loss','info','Some counters decreased or reset',
                ', '.join(item['reset_counters'][:10]),
                'Counters that decreased were excluded from rate calculations.',
                'Repeat sampling after the driver or interface stabilizes.', 'high')
    return out


def check_report(system, requested=None, duration=1.0, focus='all', include_all=False, traffic_source='auto'):
    devs=relevant_devices(system,requested,include_all)
    state,elapsed=collect_state(system,devs,duration,vendors=True,traffic_source=traffic_source)
    findings=[]
    for dev in devs:
        findings.extend(analyze_device(system,dev,state[dev],elapsed,focus))
    findings.sort(key=lambda f:({'warning':0,'info':1}.get(f['severity'],2),f['device'],f['code']))
    return {'version':VERSION, 'sample_seconds':round(elapsed,3), 'devices':devs,
            'findings':findings, 'rates':{dev:state[dev]['rates'] for dev in devs},
            'limitations':['Counter source: PHY=physical port (may include traffic not attributable to this PF); vPort=PF; netdev=Linux host interface. Domains are not additive.',
                           'Receiver-only counters cannot account for packets lost upstream of the receiver MAC.',
                           'Vendor counters may be port-wide or overlap other counters; deltas are not automatically additive.',
                           'IRQ labels are channel hints, not independently verified NAPI-to-queue mappings.']}


def status_report(system, requested=None, include_all=False):
    devs=relevant_devices(system,requested,include_all)
    rows=[]
    for dev in devs:
        info=system.if_info(dev)
        channels=((info['channels'] or {}).get('current') or {}).get('combined')
        rows.append({'device':dev, 'state':info.get('operstate'), 'driver':info.get('driver'),
                     'speed_mbps':info.get('speed_mbps'),'pci':info.get('pci'),
                     'numa':info.get('numa_node'), 'rx_queues':len(info['rx_queues']),
                     'tx_queues':len(info['tx_queues']), 'combined_channels':channels,
                     'xdp':info.get('xdp')})
    return {'version':VERSION,'interfaces':rows,
            'note':'Instantaneous inventory only. Use check for sampled error/drop deltas.'}


def explain_report(system,dev):
    info=system.if_info(dev)
    irqs=system.iface_irqs(dev)
    rss=system.rss(dev)
    groups={q:rss.count(q) for q in sorted(set(rss))} if rss is not None else None
    combined=((info['channels'] or {}).get('current') or {}).get('combined')
    return {'device':dev,'pci_chain':[i['pci'] for i in info['pci_chain']],
            'driver':info['driver'], 'numa':info['numa_node'], 'local_cpus':info.get('local_cpus'),
            'rss_weights':groups, 'rss_entries':len(rss) if rss is not None else None,
            'rx_queues':info['rx_queues'], 'tx_queues':info['tx_queues'], 'combined_channels':combined,
            'queue_irq_labels':[{'channel_hint':x['channel_index_hint'],'irq':x['irq'],
                                 'effective_cpus':x['effective_affinity'],'pci_member':x['pci_member']}
                                for x in queue_irqs(irqs)],
            'unknown_irqs':[x['irq'] for x in irqs if x not in queue_irqs(irqs)],
            'xdp':info['xdp'],
            'limitations':['RSS weights describe an indirection table, not measured packets per queue.',
                           'IRQ channel labels are hints; the queue/NAPI/IRQ mapping is not independently proven.',
                           'XDP usually runs in the RX driver/NAPI path; effective CPU may differ due to polling or busy-poll.']}


def core_aware_assignment(system, local_cpus, irqs, used_cores, avoid, allow_smt=False):
    online=set(system.online_cpus())
    eligible=sorted(set(local_cpus)&online-set(avoid))
    topology=system.cpu_topology(eligible)
    by_core={}
    for cpu in eligible:
        key=physical_key(topology,cpu)
        if key is not None and key not in used_cores:
            by_core.setdefault(key,[]).append(cpu)
    if not by_core:
        raise DoctorError('no eligible, identifiable local physical cores available; use --cpus for explicit selection')
    irqs=sorted(irqs,key=lambda x:x['channel_index_hint'])
    selected=[None]*len(irqs)
    taken=set()
    # Preserve existing good placements when possible to avoid unnecessary changes.
    for i,irq in enumerate(irqs):
        current=as_cpu_set(irq.get('effective_affinity'))
        if len(current)!=1:
            continue
        cpu=next(iter(current))
        key=physical_key(topology,cpu)
        if cpu in eligible and key in by_core and key not in taken:
            selected[i]=cpu
            taken.add(key)
    preferred=sorted(eligible, key=lambda cpu:(cpu==0,cpu))
    for i in range(len(selected)):
        if selected[i] is not None:
            continue
        for cpu in preferred:
            key=physical_key(topology,cpu)
            if key in by_core and key not in taken:
                selected[i]=cpu
                taken.add(key)
                break
    notes=[]
    if any(x is None for x in selected):
        if not allow_smt:
            raise DoctorError(f'{len(irqs)} queue IRQs but only {len(by_core)} eligible local physical cores; use --allow-smt or --cpus')
        remaining=[cpu for cpu in preferred if cpu not in selected and physical_key(topology,cpu) in by_core]
        for i in range(len(selected)):
            if selected[i] is None and remaining:
                selected[i]=remaining.pop(0)
        if any(x is None for x in selected):
            raise DoctorError(f'not enough eligible local logical CPUs for {len(irqs)} queue IRQs')
        notes.append('SMT siblings are used because distinct available physical cores were insufficient.')
    for cpu in selected:
        used_cores.add(physical_key(topology,cpu))
    return selected,notes


def optimize_report(system, requested=None, goal='balanced', user_cpus=None, avoid_cpus=None,
                    allow_smt=False, include_all=False):
    devices=relevant_devices(system,requested,include_all)
    report={'version':VERSION,'goal':goal,'devices':devices,'plans':[],
            'limitations':['This is an IRQ-affinity placement proposal, not a measured PPS/latency optimum.',
                           'RSS/channel counts and RPS/XPS are not changed automatically.',
                           'IRQ channel labels do not prove NAPI or hardware RX-queue identity.']}
    avoid=set(avoid_cpus or [])
    used_cores=set()
    if requested:
        # Respect IRQ placement already used by other interfaces in this single-device plan.
        for other in system.devices():
            if other==requested:
                continue
            for irq in queue_irqs(system.iface_irqs(other)):
                current=as_cpu_set(irq.get('effective_affinity'))
                if len(current)!=1:
                    continue
                cpu=next(iter(current))
                key=physical_key(system.cpu_topology([cpu]),cpu)
                if key is not None:
                    used_cores.add(key)
    for dev in devices:
        plan={'device':dev,'status':'blocked','selected_cpus':[], 'changes':[], 'warnings':[],
              'error':None,'source':'pci-labelled channel IRQs + online NUMA/CPU topology'}
        report['plans'].append(plan)
        try:
            info=system.if_info(dev)
            if not info.get('pci'):
                raise DoctorError('no PCI device; hardware IRQ placement cannot be established')
            irqs=system.active_irqs(dev)
            if not all(x['pci_member'] for x in irqs):
                raise DoctorError('channel-labelled IRQs are not all verified PCI MSI-X vectors')
            if user_cpus is not None:
                cpus=list(user_cpus)
                check_cpus(system,cpus)
                if len(cpus)<len(irqs):
                    raise DoctorError(f'{len(irqs)} channel IRQs but only {len(cpus)} explicit CPUs')
                selected=cpus[:len(irqs)]
                plan['source']='explicit --cpus override'
                local=set(system.numa_cpus(info['numa_node'])) if info.get('numa_node') not in (None,'-1') else set()
                if local and any(c not in local for c in selected):
                    plan['warnings'].append('Some explicitly selected CPUs are outside the local NUMA node.')
                if set(selected)&avoid:
                    raise DoctorError('explicit --cpus overlaps --avoid-cpus')
                # Reserve explicit assignments for subsequent devices in this plan.
                topo=system.cpu_topology(selected)
                used_cores.update(key for cpu in selected
                                  for key in [physical_key(topo,cpu)] if key is not None)
            else:
                node=info.get('numa_node')
                if node in (None,'-1'):
                    raise DoctorError('NUMA locality unavailable; supply --cpus explicitly')
                local=system.numa_cpus(node)
                if not local:
                    raise DoctorError('NUMA CPU list unavailable; supply --cpus explicitly')
                selected,notes=core_aware_assignment(system,local,irqs,used_cores,avoid,allow_smt)
                plan['warnings'].extend(notes)
            actions=pin_actions(system,dev,selected)
            plan['selected_cpus']=selected
            plan['changes']=actions
            plan['status']='planned' if actions else 'unchanged'
            if irqbalance_active():
                plan['warnings'].append('irqbalance is active and may override manual IRQ affinity.')
            if goal!='balanced':
                plan['warnings'].append(f'Goal {goal!r} requires workload measurement; this plan only improves CPU placement constraints.')
        except DoctorError as exc:
            plan['error']=str(exc)
    return report


def print_findings(data):
    counts={level:sum(f['severity']==level for f in data['findings']) for level in ('warning','info')}
    report_header('CHECK',f'Interfaces {len(data["devices"])}  |  Sample {data["sample_seconds"]:.2f}s  |  Warnings {counts["warning"]}, info {counts["info"]}')
    if not data['findings']:
        print('No findings from the available checks; this does not establish zero packet loss.')
    for item in data['findings']:
        print(f'[{item["severity"].upper()}] {item["device"]}  {item["title"]} ({item["code"]})')
        print(f'  Evidence: {item["evidence"]}')
        print(f'  Meaning:  {item["explanation"]}')
        print(f'  Next:     {item["recommendation"]}')
        print(f'  Confidence: {item["confidence"]}\n')
    if data['rates']:
        print('MEASURED RATES (counter-derived)')
        table([[dev, human_rate(rates['rx_pps'], 'pps'), human_rate(rates['tx_pps'], 'pps'),
                human_rate(rates['rx_bps'], 'bps'), human_rate(rates['tx_bps'], 'bps'),
                rates['rx_source'] if rates['rx_source']==rates['tx_source'] else
                f"RX:{rates['rx_source'] or '-'} TX:{rates['tx_source'] or '-'}"]
               for dev,rates in data['rates'].items()],
              ['DEVICE','RX rate','TX rate','RX bandwidth','TX bandwidth','COUNTERS'])
        print()
    for text in data['limitations']:
        print('Note:',text)


def print_status(data):
    report_header('STATUS',f'Interfaces {len(data["interfaces"])}')
    table([[x['device'],x['state'],x['driver'],x['speed_mbps'],x['numa'],
            x['combined_channels'],x['rx_queues'],x['tx_queues']]
           for x in data['interfaces']],['DEVICE','LINK','DRIVER','Mbps','NUMA','CH','RXQ','TXQ'])
    print('\n'+data['note'])
    print('Next: nic-doctor check')


def print_explain(data):
    report_header('EXPLAIN',f'Interface {data["device"]}')
    chain=' → '.join(data['pci_chain']) if data['pci_chain'] else 'unknown'
    print('HARDWARE')
    print('  PCI path: '+chain)
    print(f'  Driver: {data["driver"] or "unknown"}; NUMA: {data["numa"] or "unknown"}; local CPUs: {data["local_cpus"] or "unknown"}')
    print('DATAPATH')
    print(f'  RX queues: {cpulist(data["rx_queues"]) or "unknown"}; combined channels: {data["combined_channels"] or "unknown"}')
    print(f'  RSS slots: {data["rss_entries"] if data["rss_entries"] is not None else "unknown"}; queue weights: {data["rss_weights"] if data["rss_weights"] is not None else "unknown"}')
    for irq in data['queue_irq_labels']:
        print(f'  channel label {irq["channel_hint"]} → IRQ {irq["irq"]} → CPUs {irq["effective_cpus"] or "unknown"} (label hint)')
    if not data['queue_irq_labels']:
        print('  No verified PCI-member channel-labelled IRQs')
    print(f'  Other IRQs: {data["unknown_irqs"]}; XDP: {data["xdp"] or "not reported"}')
    print(f'  TX queues: {cpulist(data["tx_queues"]) or "unknown"}')
    for note in data['limitations']:
        print('Note:',note)
    print(f'Next: nic-doctor check {data["device"]} --focus placement')


def print_optimize(data):
    report_header('OPTIMIZE',f'Goal {data["goal"]}  |  Interfaces {len(data["devices"])}  |  Plan only')
    for item in data['plans']:
        print(f'{item["device"]}: {item["status"].upper()}')
        if item['error']:
            print('  Blocked:',item['error'])
        if item['selected_cpus']:
            print('  Proposed IRQ CPUs:',cpulist(item['selected_cpus']))
            print('  Mapping source:',item['source'])
        if item['changes']:
            plan_print(item['changes'])
        elif not item['error']:
            print('  No IRQ affinity changes needed')
        for note in item['warnings']:
            print('  Note:',note)
        print()
    for limitation in data['limitations']:
        print('Note:',limitation)
    print('Use --apply to execute supported IRQ affinity changes; verify and compare under a controlled workload.')
