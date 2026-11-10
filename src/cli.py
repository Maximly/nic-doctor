# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
def parser_build():
    p=argparse.ArgumentParser(prog='nic-doctor',description='Topology-aware Linux NIC diagnostics and guarded tuning')
    p.add_argument('--version',action='version',version=f'nic-doctor {VERSION}\n{COPYRIGHT}\nLicense: {LICENSE_ID}')
    sub=p.add_subparsers(dest='command')
    def cmd(name,description): return sub.add_parser(name,help=description)
    def j(q): q.add_argument('--json',action='store_true',help='structured JSON output')
    def apply(q,disrupt=False):
        q.add_argument('--apply',action='store_true',help='actually change the system; default is dry run')
        if disrupt: q.add_argument('--accept-disruption',action='store_true',help='acknowledge potential traffic disruption')
    q=cmd('status','concise NIC inventory; no traffic sampling');q.add_argument('device',nargs='?');q.add_argument('--all',action='store_true',help='include virtual/loopback interfaces');j(q)
    q=cmd('check','check NIC topology, IRQs, RSS and sampled drop counters');q.add_argument('device',nargs='?');q.add_argument('--duration',type=float,default=1.0,help='sample time in seconds, 0 disables delta sampling');q.add_argument('--focus',choices=['all','loss','rss','placement','pcie','link'],default='all');q.add_argument('--all',action='store_true');q.add_argument('--traffic-source',choices=['auto','phy','vport','netdev'],default='auto',help='traffic counter domain; auto prefers PHY, then complete vPort, then netdev');q.add_argument('--strict',action='store_true',help='exit 2 if warnings are detected');j(q)
    q=cmd('explain','explain the observed packet path for an interface');q.add_argument('device');j(q)
    q=cmd('optimize','preview NUMA/physical-core-aware IRQ affinity mapping');q.add_argument('device',nargs='?');q.add_argument('--goal',choices=['balanced','max-pps','max-throughput','low-latency','cpu-efficient'],default='balanced');q.add_argument('--cpus',help='explicit ordered IRQ CPU list');q.add_argument('--avoid-cpus',help='exclude CPU list from automatic placement');q.add_argument('--allow-smt',action='store_true',help='permit SMT sibling CPU sharing if required');q.add_argument('--all',action='store_true');q.add_argument('--allow-irqbalance',action='store_true');q.add_argument('--profile-out',metavar='FILE',help='write a compatible, explicit JSON IRQ profile');apply(q);j(q)
    q=cmd('list','enumerate Linux NICs'); j(q)
    q=cmd('show','interface details; omit device to show all, or use quoted glob');q.add_argument('devices',nargs='*',metavar='DEVICE');j(q)
    q=cmd('help','show general help or help for a specific command');q.add_argument('topic',nargs='?',metavar='COMMAND')
    q=cmd('topology','hardware/network/CPU/datapath topology');q.add_argument('--device');q.add_argument('--view',choices=['hardware','network','cpu','datapath'],default='hardware');q.add_argument('--format',choices=['text','json','dot'],default='text');q.add_argument('--json',action='store_true',help='alias for --format json')
    q=cmd('cpu-map','IRQ affinities and channel-label hints');q.add_argument('device');j(q)
    q=cmd('rss','show RSS or safely rebalance a contiguous queue range');q.add_argument('device');q.add_argument('--rebalance',action='store_true');q.add_argument('--queues');apply(q,True);j(q)
    q=cmd('channels','show/set combined channel count');q.add_argument('device');q.add_argument('--combined',type=int);apply(q,True);j(q)
    q=cmd('pin','pin confidently labelled NIC IRQs to CPUs');q.add_argument('device');q.add_argument('--cpus',required=True);q.add_argument('--irqs',help='explicit ordered channel-labelled PCI IRQs');q.add_argument('--strategy',choices=['one-per-queue'],default='one-per-queue');q.add_argument('--allow-irqbalance',action='store_true');apply(q)
    q=cmd('rps','show/disable RPS for all RX queues');q.add_argument('device');q.add_argument('--disable',action='store_true');apply(q);j(q)
    q=cmd('xps','show/set XPS CPU mapping for TX queues');q.add_argument('device');q.add_argument('--cpus');apply(q);j(q)
    q=cmd('stats','standard + optional vendor counters');q.add_argument('device');q.add_argument('--all',action='store_true');j(q)
    q=cmd('watch','sample packet and error counter deltas');q.add_argument('device');q.add_argument('--interval',type=float,default=1.0);q.add_argument('--count',type=int,default=5);q.add_argument('--traffic-source',choices=['auto','phy','vport','netdev'],default='auto')
    q=cmd('diagnose','correlate CPU, RSS and sampled drop counters');q.add_argument('device');q.add_argument('--duration',type=float,default=1.0);j(q)
    q=cmd('snapshot','save snapshot or show current state');q.add_argument('action',choices=['save','show']);q.add_argument('file',nargs='?');q.add_argument('--device');q.add_argument('--full',action='store_true')
    q=cmd('diff','compare two JSON snapshots or one snapshot with live host');q.add_argument('before');q.add_argument('after',nargs='?')
    q=cmd('profile','plan/apply/verify a JSON profile');q.add_argument('action',choices=['plan','apply','verify']);q.add_argument('file');q.add_argument('--allow-irqbalance',action='store_true');q.add_argument('--accept-disruption',action='store_true')
    q=cmd('rollback','restore previous transaction (best effort for dynamic driver state)');q.add_argument('id',nargs='?')
    cmd('remove','uninstall the installed NIC Doctor executable (keep saved state)')
    return p


def main(argv=None, system=None):
    p=parser_build(); a=p.parse_args(argv)
    if a.command is None:
        p.print_help()
        return 0
    if a.command == 'help':
        if a.topic is None:
            p.print_help()
        else:
            command_action = next(x for x in p._actions if isinstance(x, argparse._SubParsersAction))
            command_parser = command_action.choices.get(a.topic)
            if command_parser is None:
                raise DoctorError(f'unknown command {a.topic!r}; run nic-doctor help')
            command_parser.print_help()
        return 0
    if a.command == 'remove': remove_install();return 0
    if sys.platform != 'linux': raise DoctorError('NIC Doctor supports Linux only')
    s=system or System()
    if a.command == 'status':
        data=status_report(s,a.device,a.all)
        if a.json: out_json(data)
        else: print_status(data)
    elif a.command == 'check':
        data=check_report(s,a.device,a.duration,a.focus,a.all,a.traffic_source)
        if a.json: out_json(data)
        else: print_findings(data)
        if a.strict and any(item['severity']=='warning' for item in data['findings']):
            return 2
    elif a.command == 'explain':
        data=explain_report(s,a.device)
        if a.json: out_json(data)
        else: print_explain(data)
    elif a.command == 'optimize':
        cpus=parse_cpulist(a.cpus) if a.cpus else None
        avoid=parse_cpulist(a.avoid_cpus) if a.avoid_cpus else None
        data=optimize_report(s,a.device,a.goal,cpus,avoid,a.allow_smt,a.all)
        blocked=[item for item in data['plans'] if item['status']=='blocked']
        if a.profile_out:
            if blocked:raise DoctorError('cannot write profile with blocked devices; inspect optimize output first')
            obj={'devices':{item['device']:{'irq':{'cpus':cpulist(item['selected_cpus']),'strategy':'one-per-queue'}}
                            for item in data['plans'] if item['selected_cpus']}}
            if not obj['devices']:raise DoctorError('no usable CPU mappings for profile')
            Path(a.profile_out).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
        if a.json: out_json(data)
        else: print_optimize(data)
        if a.apply:
            if blocked:raise DoctorError('refusing partial apply: one or more device plans are blocked')
            if irqbalance_active() and not a.allow_irqbalance:
                raise DoctorError('irqbalance is active; stop/configure it or supply --allow-irqbalance')
            actions=[action for item in data['plans'] for action in item['changes']]
            transaction(s,actions,'optimize: '+a.goal)
        elif blocked:
            return 2
    elif a.command == 'list':
        data=[s.if_info(d) for d in s.devices()]
        if a.json:out_json(data)
        else:
            report_header('LIST', f'Interfaces {len(data)}')
            table([[x['device'],x['driver'],x['pci'],x['numa_node'],x['speed_mbps'] if x.get('speed_mbps') not in (None,'-1','0') else None,x['operstate']] for x in data],['IFACE','DRIVER','PCI','NUMA','Mbps','STATE'])
    elif a.command == 'show':
        from fnmatch import fnmatchcase
        known=s.devices()
        requested=a.devices
        if not requested or requested in (['all'], ['*']):
            selected=known
        else:
            selected=[]
            for item in requested:
                if item in ('all', '*'):
                    raise DoctorError("'all' and '*' must be the only device selector")
                matches=([d for d in known if fnmatchcase(d,item)]
                         if any(ch in item for ch in '*?[') else
                         [item] if item in known else [])
                if not matches:
                    suffix=(" Shell expanded '*' into filenames; use 'nic-doctor show' "
                            "or 'nic-doctor show \"*\"'." if len(requested)>1 else "")
                    raise DoctorError(f'unknown interface or unmatched glob {item!r}.{suffix}')
                for dev in matches:
                    if dev not in selected:
                        selected.append(dev)
        data=[s.if_info(dev) for dev in selected]
        if a.json:
            out_json(data if len(data)!=1 else data[0])
        elif not data:
            print('No network interfaces found')
        else:
            report_header('SHOW', f'Interfaces {len(data)}')
            for info in data:
                show_text(info)
    elif a.command == 'topology':display_topology(s,a)
    elif a.command == 'cpu-map':
        irqs=s.iface_irqs(a.device)
        if a.json:out_json({'device':a.device,'irqs':irqs,'note':'Channel indices are hints based on driver labels; not proven NAPI IDs.'})
        else:
            report_header('CPU MAP', f'Interface {a.device}  |  IRQs {len(irqs)}')
            table([[i['irq'],i['channel_index_hint'],i['affinity'],i['effective_affinity'],i['interrupts'],i['name']] for i in irqs],['IRQ','CH-HINT','CONFIG-CPU','EFFECTIVE','COUNT','NAME'])
    elif a.command == 'rss':
        if not a.rebalance:
            result=s.rss(a.device)
            if a.json:out_json({'device':a.device,'table':result,'equal_model':rss_equal_model(result)})
            else: print(f'RSS entries={len(result) if result else "unavailable"}, distribution={dict((q,result.count(q)) for q in sorted(set(result))) if result else "unknown"}')
        else:
            if not a.queues:raise DoctorError('--rebalance requires --queues 0-13')
            action=rss_action(s,a.device,parse_cpulist(a.queues))
            plan_print([action]);
            if a.apply:transaction(s,[action],f'rss {a.device}',a.accept_disruption)
            else:print('Dry run; use --apply --accept-disruption')
    elif a.command == 'channels':
        if a.combined is None:
            result=s.if_info(a.device)['channels']
            if a.json:out_json(result)
            else:print(json.dumps(result,indent=2))
        else:
            act=channel_action(s,a.device,a.combined);plan_print([act])
            if a.apply:transaction(s,[act],f'channels {a.device}',a.accept_disruption)
            else:print('Dry run; use --apply --accept-disruption')
    elif a.command == 'pin':
        if a.apply and irqbalance_active() and not a.allow_irqbalance:
            raise DoctorError('irqbalance active; stop/configure it or supply --allow-irqbalance')
        acts=pin_actions(s,a.device,parse_cpulist(a.cpus),a.irqs);plan_print(acts)
        if a.apply:transaction(s,acts,f'pin {a.device}')
        else:print('Dry run; use --apply')
    elif a.command == 'rps':
        if not a.disable:
            data=s.queue_maps(a.device,'rx','rps_cpus')
            if a.json:out_json(data)
            else:print(json.dumps(data,indent=2))
        else:
            acts=queue_actions(s,a.device,[],'rx','rps_cpus');plan_print(acts)
            if a.apply:transaction(s,acts,f'rps disable {a.device}')
            else:print('Dry run; use --apply')
    elif a.command == 'xps':
        if a.cpus is None:
            data=s.queue_maps(a.device,'tx','xps_cpus')
            if a.json:out_json(data)
            else:print(json.dumps(data,indent=2))
        else:
            cpus=parse_cpulist(a.cpus);check_cpus(s,cpus)
            acts=queue_actions(s,a.device,cpus,'tx','xps_cpus');plan_print(acts)
            if a.apply:transaction(s,acts,f'xps {a.device}')
            else:print('Dry run; use --apply')
    elif a.command == 'stats':
        data=s.counters(a.device,a.all)
        if a.json:out_json(data)
        else:
            report_header('STATS', f'Interface {a.device}  |  Counters {len(data)}')
            table([[k,v] for k,v in data.items()],['COUNTER','VALUE'])
    elif a.command == 'watch':
        if a.interval<=0 or a.interval>3600 or a.count<1 or a.count>100000:raise DoctorError('invalid watch interval/count')
        prev=s.counters(a.device,True)
        last=time.monotonic()
        print('interval  RX rate      TX rate      RX bandwidth  TX bandwidth  counters')
        for _ in range(a.count):
            time.sleep(a.interval)
            curr=s.counters(a.device,True)
            now=time.monotonic()
            elapsed=now-last
            delta={k:curr[k]-v for k,v in prev.items() if k in curr and curr[k]>=v}
            hot={k:v for k,v in delta.items() if v>0 and DROP_RE.search(k)}
            rates=traffic_rates(delta,elapsed,a.traffic_source)
            rx_src=rates['rx_source'] or '-'
            tx_src=rates['tx_source'] or '-'
            print(f"{elapsed:7.2f}s  {human_rate(rates['rx_pps'],'pps'):12} "
                  f"{human_rate(rates['tx_pps'],'pps'):12} "
                  f"{human_rate(rates['rx_bps'],'bps'):13} "
                  f"{human_rate(rates['tx_bps'],'bps'):13} "
                  f"{rx_src if rx_src==tx_src else 'RX:'+rx_src+' TX:'+tx_src}; {len(hot)} error counters")
            prev,last=curr,now
    elif a.command == 'diagnose':
        if a.duration<0 or a.duration>300:raise DoctorError('--duration must be 0..300s')
        data=diagnose(s,a.device,a.duration)
        if a.json:out_json(data)
        else:
            report_header('DIAGNOSE', f'Interface {a.device}  |  {len(data["warnings"])} findings')
            for x in data['warnings']:print('  WARN:',x)
            for x in data['limits']:print('  NOTE:',x)
            print('  Deltas:',json.dumps(data['counter_deltas'],sort_keys=True))
    elif a.command == 'snapshot':
        data=s.snapshot([a.device] if a.device else None,a.full)
        if a.action == 'save':
            if not a.file:raise DoctorError('snapshot save requires filename')
            file=Path(a.file);file.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
            print(f'Saved {file}')
        else:out_json(data)
    elif a.command == 'diff':
        try:
            before=json.loads(Path(a.before).read_text());after=json.loads(Path(a.after).read_text()) if a.after else s.snapshot()
        except (OSError,ValueError) as exc:raise DoctorError(f'snapshot read failed: {exc}')
        changes=diff_dict(before,after)
        for path,x,y in changes[:200]:print(f'{path}: {x} -> {y}')
        print(f'{len(changes)} differences'+(' (first 200 shown)' if len(changes)>200 else ''))
    elif a.command == 'profile':
        obj=profile_load(a.file)
        if a.action == 'apply':
            a.apply=True;profile_apply(s,obj,a)
        elif a.action == 'plan':
            a.apply=False;profile_apply(s,obj,a)
        else:
            any_diff=False
            for dev,spec in obj['devices'].items():
                acts=profile_actions(s,dev,spec)
                if acts:
                    any_diff=True;print(f'{dev}: DRIFT');plan_print(acts)
                else:print(f'{dev}: MATCH')
            if any_diff:return 2
    elif a.command == 'rollback':roll_back(s,a.id)
    return 0


if __name__=='__main__':
    try:
        sys.exit(main())
    except (DoctorError, KeyError, ValueError, TypeError) as exc:
        print(f'nic-doctor: {exc}',file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nInterrupted',file=sys.stderr)
        sys.exit(130)
