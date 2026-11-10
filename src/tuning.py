# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
def require_root():
    if os.geteuid() != 0:
        raise DoctorError('root required for --apply, rollback and remove (use sudo)')


def irqbalance_active():
    return (run('systemctl', 'is-active', 'irqbalance') or '').strip() == 'active'


def irq_mapping(system, dev, cpus, explicit=None):
    if explicit:
        irqnums = parse_cpulist(explicit)
        all_ids = {x['irq'] for x in system.iface_irqs(dev) if x['pci_member']}
        if not set(irqnums).issubset(all_ids):
            raise DoctorError('explicit IRQ(s) must belong to this PCI device; no unverified vectors permitted')
        items = [next(x for x in system.iface_irqs(dev) if x['irq'] == irq) for irq in irqnums]
        if any(x['channel_index_hint'] is None for x in items):
            raise DoctorError('explicit IRQ list includes non-channel/async vectors; refuse to pin')
    else:
        items = system.active_irqs(dev)
    if not items:
        raise DoctorError('no channel IRQs found')
    if len(cpus) < len(items):
        raise DoctorError(f'{len(items)} channel IRQs but only {len(cpus)} CPUs; need at least one CPU per IRQ')
    return [(x, cpus[i % len(cpus)]) for i,x in enumerate(items)]


def check_cpus(system, cpus):
    missing = set(cpus) - set(system.online_cpus())
    if missing:
        raise DoctorError(f'CPUs offline or unavailable: {cpulist(missing)}')


def file_op(path, new, old):
    if old is None:
        raise DoctorError(f'unavailable control file: {path}')
    before, after = old.strip(), new.strip()
    if str(path).endswith(('rps_cpus','xps_cpus')) and set(mask_cpus(before)) == set(mask_cpus(after)):
        after = before  # kernel masks are sometimes formatted as 0 vs 00000000
    return {'kind':'file', 'path':str(path), 'before':before, 'after':after}


def pin_actions(system, dev, cpus, explicit=None):
    system.device(dev)
    check_cpus(system, cpus)
    actions = []
    for item,cpu in irq_mapping(system, dev, cpus, explicit):
        path = system.procroot / f'irq/{item["irq"]}/smp_affinity_list'
        actions.append(file_op(path, str(cpu), read(path)))
    return [a for a in actions if a['before'] != a['after']]


def queue_actions(system, dev, cpus, direction, key):
    p = system.device(dev) / 'queues'
    paths = sorted(p.glob(f'{direction}-[0-9]*/{key}'), key=lambda x:int(x.parent.name.split('-')[-1]))
    if not paths:
        raise DoctorError(f'{dev}: no {key} controls found')
    actions=[]
    for i, path in enumerate(paths):
        value = cpu_mask([cpus[i % len(cpus)]]) if cpus else '00000000'
        actions.append(file_op(path, value, read(path)))
    return [a for a in actions if a['before'] != a['after']]


def channel_action(system, dev, count):
    chans = ethtool_channels(run('ethtool', '-l', dev))
    if not chans or chans['current'].get('combined') is None:
        raise DoctorError(f'{dev}: ethtool combined channels not supported')
    maximum = chans['maximum'].get('combined')
    if count < 1 or (maximum and count > maximum):
        raise DoctorError(f'combined channel count must be within 1..{maximum}')
    return {'kind':'channels', 'device':dev, 'before':chans['current']['combined'], 'after':count}


def rss_action(system, dev, queues):
    original = system.rss(dev)
    if original is None:
        raise DoctorError(f'{dev}: RSS indirection table not readable; cannot guarantee rollback')
    before = rss_equal_model(original)
    if not before:
        raise DoctorError(f'{dev}: original RSS layout is not representable by ethtool equal/start; exact rollback unavailable, refusing change')
    if not queues or queues != list(range(queues[0], queues[-1]+1)):
        raise DoctorError('RSS queues must be a contiguous range')
    chans = ethtool_channels(run('ethtool', '-l', dev))
    current = (chans or {}).get('current', {}).get('combined')
    if current is not None and queues[-1] >= current:
        raise DoctorError(f'RSS queue {queues[-1]} is outside current combined channels 0..{current-1}')
    return {'kind':'rss', 'device':dev, 'before':before,
            'after':{'start':queues[0], 'equal':len(queues)}, 'entries':len(original)}


def allowed_action(system, action):
    kind = action.get('kind')
    if kind == 'file':
        p = Path(action['path'])
        path = str(p)
        proc_prefix = re.escape(str(system.procroot))
        sys_prefix = re.escape(str(system.netroot))
        if re.fullmatch(proc_prefix + r'/irq/\d+/smp_affinity_list', path):
            return True
        if re.fullmatch(sys_prefix + r'/[A-Za-z0-9_.:@-]+/queues/(?:rx-\d+/rps_cpus|tx-\d+/xps_cpus)', path):
            system.device(p.parts[len(system.netroot.parts)])
            return True
        raise DoctorError(f'unsafe/unrecognized write target: {path}')
    if kind in ('channels', 'rss'):
        system.device(action['device'])
        return True
    raise DoctorError(f'unsupported action kind: {kind}')


def ethtool_rss_set(dev, spec):
    cmd = ['ethtool', '-X', dev]
    if spec['start']:
        cmd += ['start', str(spec['start'])]
    cmd += ['equal', str(spec['equal'])]
    return cmd


def change(system, action, reverse=False):
    allowed_action(system, action)
    target = action['before'] if reverse else action['after']
    if action['kind'] == 'file':
        try:
            Path(action['path']).write_text(str(target)+'\n')
        except OSError as exc:
            raise DoctorError(f"cannot write {action['path']}: {exc}") from exc
        got = read(action['path'])
        if action['path'].endswith(('rps_cpus', 'xps_cpus')):
            match = set(mask_cpus(got)) == set(mask_cpus(target))
        elif action['path'].endswith('smp_affinity_list'):
            match = set(parse_cpulist(got)) == set(parse_cpulist(str(target))) if got else False
            effective = read(Path(action['path']).with_name('effective_affinity_list'))
            if effective:
                match = match and set(parse_cpulist(effective)) == set(parse_cpulist(str(target)))
        else:
            match = got == str(target)
        if not match:
            raise DoctorError(f'verification failed for {action["path"]}: requested={target}, actual={got}')
    elif action['kind'] == 'channels':
        cmd = ['ethtool','-L', action['device'], 'combined', str(target)]
        if run(*cmd,timeout=20) is None:
            raise DoctorError('channel set failed: ' + ' '.join(cmd))
        cur = ethtool_channels(run('ethtool','-l',action['device']))
        if not cur or cur['current'].get('combined') != target:
            raise DoctorError(f'channel verify failed on {action["device"]}')
    elif action['kind'] == 'rss':
        cmd = ethtool_rss_set(action['device'], target)
        if run(*cmd, timeout=15) is None:
            raise DoctorError('RSS set failed: ' + ' '.join(cmd))
        now = system.rss(action['device'])
        expected = [target['start'] + (i % target['equal']) for i in range(action['entries'])]
        if now != expected:
            raise DoctorError(f'RSS verification failed on {action["device"]}; driver did not retain requested table')


@contextmanager
def system_lock(system):
    require_root()
    system.state.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = system.state/'lock'
    with os.fdopen(os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600), 'r+') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise DoctorError('another nic-doctor write/rollback is active')
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def transaction(system, actions, description, allow_disruption=False):
    with system_lock(system):
        return _transaction_locked(system, actions, description, allow_disruption)


def _transaction_locked(system, actions, description, allow_disruption=False):
    require_root()
    if any(a['kind'] in ('channels','rss') for a in actions) and not allow_disruption:
        raise DoctorError('channel/RSS modifications can interrupt traffic; supply --accept-disruption')
    actions = [a for a in actions if a['before'] != a['after']]
    for a in actions:
        allowed_action(system,a)
    if not actions:
        print('No changes required')
        return None
    ident = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+secrets.token_hex(4)
    target = system.state/'transactions'/f'{ident}.json'
    journal = {'schema_version':1,'id':ident,'description':description,'status':'in_progress',
               'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actions':actions}
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        os.chmod(target.parent,0o700)
    except OSError:
        pass
    def save():
        tmp=target.with_suffix('.tmp')
        with os.fdopen(os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'w') as f:
            json.dump(journal,f,indent=2)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp,target)
    applied=[]
    save()
    try:
        for action in actions:
            # Include failed operations in rollback: a write may have succeeded before verification failed.
            applied.append(action)
            change(system, action)
    except Exception as exc:
        rollback_errors=[]
        for action in reversed(applied):
            try:
                change(system,action,reverse=True)
            except Exception as roll_exc:
                rollback_errors.append(str(roll_exc))
        journal['status']='failed_rollback' if rollback_errors else 'failed_reverted'
        journal['error']=str(exc)
        journal['rollback_errors']=rollback_errors
        save()
        raise DoctorError(f'apply failed: {exc}; rollback: '+('; '.join(rollback_errors) if rollback_errors else 'verified for attempted steps')) from exc
    journal['status']='applied'
    save()
    print(f'Applied and verified {len(actions)} changes. Transaction: {ident}')
    return ident


def roll_back(system, ident=None):
    with system_lock(system):
        return _roll_back_locked(system, ident)


def _roll_back_locked(system, ident=None):
    require_root()
    directory=system.state/'transactions'
    files=sorted(directory.glob('*.json')) if directory.is_dir() else []
    if ident:
        if not re.fullmatch(r'\d{8}T\d{6}Z-[0-9a-f]{8}',ident):
            raise DoctorError('invalid transaction ID')
        files=[directory/f'{ident}.json']
    if not files:
        raise DoctorError('no saved transactions')
    target=None; journal=None
    for path in reversed(files):
        try:
            obj=json.loads(path.read_text())
        except (OSError,ValueError):
            continue
        if obj.get('status') in ('applied', 'rollback_failed', 'failed_rollback'):
            target=path; journal=obj; break
    if journal is None:
        raise DoctorError('no applied transaction to rollback')
    errs=[]
    for action in reversed(journal['actions']):
        try:
            change(system,action,reverse=True)
        except Exception as exc:
            errs.append(str(exc))
    journal['status']='rollback_failed' if errs else 'rolled_back'
    if errs: journal['rollback_errors']=errs
    tmp=target.with_suffix('.tmp')
    with os.fdopen(os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'w') as f:
        json.dump(journal,f,indent=2)
    os.replace(tmp,target)
    if errs:
        raise DoctorError(f'rollback incomplete for {journal["id"]}: '+ '; '.join(errs))
    print(f'Rollback verified: {journal["id"]}')


def plan_print(actions):
    if not actions:
        print('No changes planned')
        return
    for a in actions:
        if a['kind'] == 'file':
            print(f'  {a["path"]}: {a["before"]} -> {a["after"]}')
        elif a['kind'] == 'channels':
            print(f'  ethtool -L {a["device"]} combined {a["after"]}   # was {a["before"]}')
        elif a['kind'] == 'rss':
            print(f'  {" ".join(ethtool_rss_set(a["device"], a["after"]))}   # was {a["before"]}')


def profile_load(path):
    try:
        obj=json.loads(Path(path).read_text())
    except (OSError,ValueError) as exc:
        raise DoctorError(f'cannot load JSON profile: {exc}') from exc
    if not isinstance(obj,dict) or not isinstance(obj.get('devices'),dict) or not obj['devices']:
        raise DoctorError('profile must contain nonempty "devices" object')
    allowed={'channels','irq','rss','rps','xps'}
    for d,spec in obj['devices'].items():
        if not isinstance(spec,dict) or (set(spec)-allowed):
            raise DoctorError(f'{d}: unknown or malformed profile sections {set(spec)-allowed if isinstance(spec,dict) else ""}')
    return obj


def profile_actions(system, dev, spec, skip_channels=False):
    actions=[]
    if 'channels' in spec and not skip_channels:
        actions.append(channel_action(system,dev,int(spec['channels']['combined'])))
    if 'irq' in spec:
        cfg=spec['irq']
        if cfg.get('strategy','one-per-queue') != 'one-per-queue':
            raise DoctorError('supported IRQ strategy: one-per-queue')
        actions += pin_actions(system,dev,parse_cpulist(cfg['cpus']),cfg.get('irqs'))
    if 'rss' in spec:
        cfg=spec['rss']
        if cfg.get('rebalance') is not True:
            raise DoctorError('RSS profiles require rebalance:true')
        actions.append(rss_action(system,dev,parse_cpulist(cfg['queues'])))
    if 'rps' in spec:
        cfg=spec['rps']
        if cfg.get('enabled') is not False:
            raise DoctorError('RPS profiles support enabled:false only')
        actions += queue_actions(system,dev,[], 'rx','rps_cpus')
    if 'xps' in spec:
        cfg=spec['xps']
        cpus=parse_cpulist(cfg['cpus']); check_cpus(system,cpus)
        actions += queue_actions(system,dev,cpus,'tx','xps_cpus')
    return [a for a in actions if a['before'] != a['after']]


def profile_apply(system, obj, args):
    # Channel resizing may change IRQ identities and queue indices. Apply it separately.
    actions=[]
    for dev,spec in obj['devices'].items():
        if 'channels' in spec and len(spec)>1:
            current=channel_action(system,dev,int(spec['channels']['combined']))
            if current['before'] != current['after']:
                raise DoctorError(f'{dev}: apply channel resize separately, then re-run profile apply to rediscover IRQs/queues')
        actions+=profile_actions(system,dev,spec)
    print('Profile plan:')
    plan_print(actions)
    if args.apply:
        if any('irq' in spec for spec in obj['devices'].values()) and irqbalance_active() and not args.allow_irqbalance:
            raise DoctorError('irqbalance is active; stop/configure it or supply --allow-irqbalance')
        transaction(system,actions,'profile',args.accept_disruption)
    else:
        print('Dry run. Add --apply to execute.')
    return actions


def diff_dict(a,b,prefix=''):
    changes=[]
    if isinstance(a,dict) and isinstance(b,dict):
        for key in sorted(set(a)|set(b)):
            if key in ('timestamp_utc',): continue
            changes.extend(diff_dict(a.get(key),b.get(key),f'{prefix}.{key}' if prefix else key))
    elif a != b:
        changes.append((prefix,a,b))
    return changes


def diagnose(system,dev,duration):
    info=system.if_info(dev)
    warnings=[]; evidence=[]
    irqs=system.iface_irqs(dev)
    if info['numa_node'] not in (None, '-1'):
        local=set(system.numa_cpus(info['numa_node']))
        for entry in irqs:
            try: pinned=set(parse_cpulist(entry['effective_affinity']))
            except DoctorError: pinned=set()
            if pinned and local and pinned.isdisjoint(local) and entry['channel_index_hint'] is not None:
                warnings.append(f'IRQ {entry["irq"]} (channel hint {entry["channel_index_hint"]}) entirely outside local NUMA {info["numa_node"]}')
    chans=info['channels'] or {}
    combined=chans.get('current',{}).get('combined')
    rss=system.rss(dev)
    if rss and combined:
        invalid=sorted(set(x for x in rss if x >= combined))
        if invalid:
            warnings.append(f'RSS table references queues beyond {combined} combined channels: {invalid}')
        unused=sorted(set(range(combined))-set(rss))
        if unused:
            warnings.append(f'RSS indirection has no entries for active queue indices: {unused}')
    elif rss is None:
        evidence.append('RSS table unavailable; could not validate queue distribution')
    start=system.counters(dev, True)
    if duration:
        time.sleep(duration)
    end=system.counters(dev, True)
    diffs={k:end[k]-v for k,v in start.items() if k in end and end[k]>=v}
    hot={k:v for k,v in diffs.items() if v>0 and DROP_RE.search(k)}
    for key,value in sorted(hot.items(),key=lambda x:-x[1])[:20]:
        warnings.append(f'{key}: +{value} in {duration or 0:g}s (counter meaning/scope must be checked)')
    if irqbalance_active():
        warnings.append('irqbalance active: manual IRQ affinity may be overwritten')
    if not irqs:
        evidence.append('No attributable IRQs identified; IRQ/channel mapping is unknown')
    if any(i['channel_index_hint'] is None for i in irqs):
        evidence.append('Some NIC MSI vectors are not channel-labelled; do not equate MSI vector order with RX queue index')
    if not hot:
        evidence.append('No increasing named drop/error counters observed; this does not prove loss-free delivery')
    evidence.append('Receiver-only data cannot account for traffic that never reached the receiver MAC')
    return {'device':dev,'sample_seconds':duration,'warnings':warnings,'limits':evidence,
            'counter_deltas':{k:v for k,v in diffs.items() if k in ('rx_packets','rx_bytes','tx_packets','tx_bytes','rx_dropped','tx_dropped') or k in hot}}


def remove_install():
    require_root()
    exe=Path(__file__).absolute()
    if exe.name != 'nic-doctor' or exe.parent.name != 'bin' or not exe.is_file():
        raise DoctorError('not running the installed nic-doctor binary; cannot remove')
    root=exe.parent.parent
    record=root/'lib/nic-doctor/install.json'
    if not record.is_file():
        raise DoctorError('installation manifest missing; refusing to remove arbitrary files')
    try:
        meta=json.loads(record.read_text())
    except (OSError,ValueError):
        raise DoctorError('invalid installation manifest')
    digest=hashlib.sha256(exe.read_bytes()).hexdigest()
    if (meta.get('binary') != str(exe) or meta.get('sha256') != digest or
        meta.get('marker') != 'NIC_DOCTOR_RELEASE'):
        raise DoctorError('installed file changed or manifest mismatch; refusing unattended removal')
    if exe.is_symlink() or record.is_symlink():
        raise DoctorError('symlink install path; refusing removal')
    exe.unlink()
    record.unlink()
    try: record.parent.rmdir()
    except OSError: pass
    print(f'Removed {exe}. Saved state in /var/lib/nic-doctor was not deleted.')
