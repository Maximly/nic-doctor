# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
class System:
    def __init__(self, sysroot='/sys', procroot='/proc', state=None):
        self.sysroot = Path(sysroot)
        self.procroot = Path(procroot)
        self.state = Path(state or os.environ.get('NIC_DOCTOR_STATE_DIR', '/var/lib/nic-doctor'))

    @property
    def netroot(self):
        return self.sysroot / 'class/net'

    def device(self, dev):
        if not DEVICE_RE.fullmatch(dev) or dev in ('.', '..') or '/' in dev:
            raise DoctorError('invalid interface name')
        path = self.netroot / dev
        if not path.exists():
            raise DoctorError(f'interface {dev!r} not found in {self.netroot}')
        return path

    def devices(self):
        try:
            return sorted(p.name for p in self.netroot.iterdir() if DEVICE_RE.fullmatch(p.name))
        except OSError:
            return []

    def online_cpus(self):
        v = read(self.sysroot / 'devices/system/cpu/online')
        return parse_cpulist(v) if v else list(range(os.cpu_count() or 1))

    def numa_cpus(self, node):
        val = read(self.sysroot / f'devices/system/node/node{node}/cpulist')
        return parse_cpulist(val) if val else []

    def cpu_topology(self, cpus):
        out = {}
        for cpu in cpus:
            p = self.sysroot / f'devices/system/cpu/cpu{cpu}/topology'
            out[str(cpu)] = {'socket': read(p/'physical_package_id'),
                             'core': read(p/'core_id'),
                             'siblings': read(p/'thread_siblings_list')}
        return out

    def pci_chain(self, dev):
        """Walk sysfs PCI ancestry; do not invent a PCIe root-complex or switch identity."""
        link = self.device(dev) / 'device'
        if not link.exists():
            return []
        chain = []
        for node in reversed((link.resolve(), *link.resolve().parents)):
            if re.fullmatch(r'[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]', node.name):
                chain.append({'pci': node.name, 'vendor': read(node/'vendor'),
                              'device_id': read(node/'device'), 'class': read(node/'class'),
                              'pcie_link_speed': read(node/'current_link_speed'),
                              'pcie_link_width': read(node/'current_link_width'),
                              'pcie_max_speed': read(node/'max_link_speed'),
                              'pcie_max_width': read(node/'max_link_width'),
                              'driver': (node/'driver').resolve().name if (node/'driver').exists() else None})
        return chain

    def if_info(self, dev):
        p = self.device(dev)
        pci = p / 'device'
        bdf = pci.resolve().name if pci.exists() else None
        chain = self.pci_chain(dev)
        if not re.fullmatch(r'[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]', bdf or ''):
            bdf = chain[-1]['pci'] if chain else None
        driver_path = pci / 'driver'
        ifi = run('ethtool', '-i', dev) or ''
        kv = {}
        for line in ifi.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                kv[k.strip()] = v.strip()
        try:
            rx = sorted(int(x.name.split('-')[-1]) for x in (p/'queues').glob('rx-[0-9]*'))
            tx = sorted(int(x.name.split('-')[-1]) for x in (p/'queues').glob('tx-[0-9]*'))
        except ValueError:
            rx, tx = [], []
        return {'device': dev, 'ifindex': read(p/'ifindex'), 'mac': read(p/'address'),
                'operstate': read(p/'operstate'), 'mtu': read(p/'mtu'),
                'speed_mbps': read(p/'speed'), 'pci': bdf if bdf and re.fullmatch(r'[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]', bdf) else None,
                'driver': kv.get('driver') or (driver_path.resolve().name if driver_path.exists() else None),
                'firmware': kv.get('firmware-version'), 'numa_node': read(pci/'numa_node'),
                'local_cpus': read(pci/'local_cpulist'), 'pci_chain': chain,
                'rx_queues': rx, 'tx_queues': tx,
                'channels': ethtool_channels(run('ethtool', '-l', dev)),
                'master': read(p/'master/ifindex'),
                'xdp': self.xdp(dev)}

    def xdp(self, dev):
        raw = run('ip', '-j', '-d', 'link', 'show', 'dev', dev)
        if not raw:
            return None
        try:
            arr = json.loads(raw)
            return arr[0].get('xdp') if arr else None
        except (ValueError, KeyError, TypeError):
            return None

    def iface_irqs(self, dev):
        info = self.if_info(dev)
        bdf = info['pci']
        ifpath = self.device(dev) / 'device/msi_irqs'
        irq_nums = {int(x.name) for x in ifpath.iterdir() if IRQ_RE.fullmatch(x.name)} if ifpath.is_dir() else set()
        raw = read(self.procroot / 'interrupts', '')
        result = []
        for line in raw.splitlines():
            m = re.match(r'^\s*(\d+):\s+(.*)$', line)
            if not m:
                continue
            irq = int(m.group(1))
            payload = m.group(2)
            labels = payload.split()
            label = labels[-1] if labels else ''
            if irq not in irq_nums and not re.search(r'(?<![\w])'+re.escape(dev)+r'(?![\w])', payload) and not (bdf and f'@pci:{bdf}' in payload):
                continue
            idx = None
            # NVIDIA OFED and upstream mlx5 commonly rename active completion IRQs to IFNAME-<channel>.
            # Other drivers use IFNAME-TxRx-N or IFNAME-rx-N. Do not infer from mlx5_compN.
            pattern = r'(?:^|\s)' + re.escape(dev) + r'-(?:(?:TxRx|rx|tx)-)?(\d+)(?:\s|$)'
            match = re.search(pattern, payload, flags=re.I)
            if match:
                idx = int(match.group(1))
            aff = read(self.procroot / f'irq/{irq}/smp_affinity_list')
            eff = read(self.procroot / f'irq/{irq}/effective_affinity_list')
            if eff is None:
                effmask = read(self.procroot / f'irq/{irq}/effective_affinity')
                eff = cpulist(mask_cpus(effmask)) if effmask else None
            count_cols = re.match(r'^\s*((?:\d+\s+)+)', payload)
            counts = [int(c) for c in count_cols.group(1).split()] if count_cols else []
            result.append({'irq': irq, 'name': label, 'channel_index_hint': idx,
                           'affinity': aff, 'effective_affinity': eff,
                           'interrupts': sum(counts), 'pci_member': irq in irq_nums})
        return sorted(result, key=lambda x: x['irq'])

    def active_irqs(self, dev):
        """Use only distinct, unambiguous channel-labelled IRQs, never arbitrary MSI-X vector order."""
        items = self.iface_irqs(dev)
        by = {}
        for item in items:
            idx = item['channel_index_hint']
            if idx is not None:
                if not item['pci_member']:
                    raise DoctorError(f'IRQ {item["irq"]} has a matching interface label but is not in the NIC PCI MSI-X set')
                if idx in by:
                    raise DoctorError(f'ambiguous duplicate channel-labelled IRQ {idx} on {dev}; use --irqs')
                by[idx] = item
        chans = self.if_info(dev)['channels']
        needed = (chans or {}).get('current', {}).get('combined')
        if needed is None:
            needed = len(self.if_info(dev)['rx_queues'])
        if not needed or set(by) != set(range(needed)):
            raise DoctorError(f'cannot prove IRQ↔channel mapping for {dev}: found {sorted(by)}, expected 0..{needed-1}; supply --irqs explicitly')
        return [by[i] for i in range(needed)]

    def rss(self, dev):
        self.device(dev)
        return ethtool_rss(run('ethtool', '-x', dev))

    def counters(self, dev, vendor=False):
        p = self.device(dev) / 'statistics'
        out = {}
        if p.is_dir():
            for item in sorted(p.iterdir()):
                value = read(item)
                if value is not None and re.fullmatch(r'\d+', value):
                    out[item.name] = int(value)
        if vendor:
            out.update({'ethtool/' + k: v for k, v in ethtool_stats(run('ethtool', '-S', dev)).items()})
        return out

    def snapshot(self, devices=None, full=False):
        result = {'schema_version': 1, 'tool_version': VERSION,
                  'timestamp_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                  'host': os.uname().nodename, 'devices': {}}
        for dev in (devices if devices is not None else self.devices()):
            result['devices'][dev] = {'info': self.if_info(dev), 'irqs': self.iface_irqs(dev),
                                      'rss_indirection': self.rss(dev), 'counters': self.counters(dev, full),
                                      'rps': self.queue_maps(dev, 'rx', 'rps_cpus'),
                                      'xps': self.queue_maps(dev, 'tx', 'xps_cpus')}
        return result

    def queue_maps(self, dev, direction, file):
        p = self.device(dev) / 'queues'
        out = {}
        for q in sorted(p.glob(f'{direction}-[0-9]*')):
            value = read(q/file)
            if value is not None:
                out[q.name] = value
        return out

    def network(self, devs=None):
        out = {}
        for dev in (devs or self.devices()):
            p = self.device(dev)
            out[dev] = {'master': (p/'master').resolve().name if (p/'master').exists() else None,
                        'uppers': [x.name[6:] for x in sorted(p.glob('upper_*'))],
                        'lowers': [x.name[6:] for x in sorted(p.glob('lower_*'))],
                        'iflink': read(p/'iflink'), 'ifindex': read(p/'ifindex')}
        return out
