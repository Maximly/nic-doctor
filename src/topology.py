# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
def out_json(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))


def table(rows, headers):
    data = [[str(x if x is not None else '-') for x in row] for row in rows]
    widths = [max(len(h), *(len(r[i]) for r in data)) for i,h in enumerate(headers)]
    print('  '.join(h.ljust(widths[i]) for i,h in enumerate(headers)))
    print('  '.join('-'*w for w in widths))
    for row in data:
        print('  '.join(x.ljust(widths[i]) for i,x in enumerate(row)))



def report_header(section, detail=None):
    print(f'NIC Doctor  |  {section.upper()}')
    if detail:
        print(detail)
    print()


def show_text(info):
    dev = info['device']
    print(f'DEVICE {dev}')
    print('  ' + '─' * (7 + len(dev)))
    speed = info.get('speed_mbps')
    if speed is not None:
        try:
            if int(speed) <= 0:
                speed = None
        except (TypeError, ValueError):
            pass
    sections = [
        ('DEVICE', [('Name', dev), ('MAC address', info.get('mac')),
                    ('Interface index', info.get('ifindex'))]),
        ('LINK / HEALTH', [('State', info.get('operstate')), ('MTU', info.get('mtu')),
                           ('Speed (Mbps)', speed)]),
        ('HARDWARE / NUMA', [('PCI address', info.get('pci')), ('Driver', info.get('driver')),
                            ('Firmware', info.get('firmware')), ('NUMA node', info.get('numa_node')),
                            ('Local CPUs', info.get('local_cpus'))]),
        ('DATAPATH', [('RX queues', cpulist(info.get('rx_queues') or [])),
                      ('TX queues', cpulist(info.get('tx_queues') or [])),
                      ('Combined channels', (info.get('channels') or {}).get('current',{}).get('combined')),
                      ('XDP', json.dumps(info['xdp'], sort_keys=True) if info.get('xdp') is not None else None)])]
    for heading, items in sections:
        print(heading)
        for label, value in items:
            if value is None or value == '':
                value = '-'
            print(f'  {label:<20} {value}')
        print()


def tree_node(label):
    """Ordered tree node. Siblings are merged by stable hardware identity."""
    return {'label': label, 'children': {}}


def tree_child(parent, key, label):
    children = parent['children']
    if key not in children:
        children[key] = tree_node(label)
    return children[key]


def tree_lines(root):
    """Format an ordered tree using Unicode branch characters."""
    lines = [root['label']]

    def visit(parent, prefix):
        children = list(parent['children'].values())
        for index, child in enumerate(children):
            last = index == len(children) - 1
            lines.append(prefix + ('└─ ' if last else '├─ ') + child['label'])
            visit(child, prefix + ('   ' if last else '│  '))

    visit(root, '')
    return lines


def pci_link(node):
    """Display *negotiated* and maximum links independently when available."""
    gens = {'2.5': 'Gen1', '5.0': 'Gen2', '8.0': 'Gen3',
            '16.0': 'Gen4', '32.0': 'Gen5', '64.0': 'Gen6'}

    def link(speed, width):
        if not speed or not width or not str(width).isdigit() or int(width) <= 0:
            return None
        match = re.match(r'^\s*([0-9]+(?:\.[0-9]+)?)\s+GT/s', speed)
        if not match:
            return None
        gen = gens.get(match.group(1))
        return f'{gen} x{width}' if gen else f'{match.group(1)} GT/s x{width}'

    current = link(node.get('pcie_link_speed'), node.get('pcie_link_width'))
    maximum = link(node.get('pcie_max_speed'), node.get('pcie_max_width'))
    if current and maximum:
        return f'{current} (max {maximum})'
    if current:
        return current
    return f'max {maximum}' if maximum else None


def pci_description(node):
    cls = node.get('class') or ''
    role = ('PCIe bridge' if cls.lower().startswith('0x0604') else
            'Network controller' if cls.lower().startswith('0x02') else
            'PCI device')
    bdf = node['pci']
    # Use lspci descriptions when available; otherwise display the PCI class.
    result = run('lspci', '-D', '-s', bdf)
    desc = None
    if result:
        for line in result.splitlines():
            match = re.match(r'^' + re.escape(bdf) + r'\s+(.+)$', line, re.I)
            if match:
                desc = match.group(1).strip()
                break
    label = f'{bdf[5:]} — {desc or role}'
    bits = []
    negotiated = pci_link(node)
    if negotiated:
        bits.append(negotiated)
    if node.get('driver'):
        bits.append('driver ' + node['driver'])
    if bits:
        label += ' [' + '; '.join(bits) + ']'
    return label


def nic_description(info):
    dev = info['device']
    bits = []
    if info['driver']:
        bits.append(info['driver'])
    speed = info['speed_mbps']
    if speed and speed.isdigit() and int(speed) > 0:
        rate = int(speed)
        bits.append((f'{rate//1000} Gb/s' if rate % 1000 == 0 else
                     f'{rate/1000:g} Gb/s' if rate >= 1000 else f'{rate} Mb/s'))
    if info['operstate']:
        bits.append(info['operstate'])
    if info['rx_queues'] or info['tx_queues']:
        bits.append(f'RXQ {len(info["rx_queues"])} / TXQ {len(info["tx_queues"])}')
    return dev + (' [' + '; '.join(bits) + ']' if bits else '')


def numa_group(root, info, system):
    node = info.get('numa_node')
    if node in (None, '-1') or not str(node).isdigit():
        return tree_child(root, ('numa', '?'), 'NUMA node unknown')
    cpus = system.numa_cpus(node)
    text = cpulist(cpus) if cpus else info.get('local_cpus')
    return tree_child(root, ('numa', int(node)),
                      f'NUMA node {node}' + (f' [local CPUs {text}]' if text else ''))


def topology_tree(system, devs, view, info_map, details):
    root = tree_node('Network')
    if view == 'hardware':
        # Shared PCI ancestors are grouped once; non-PCI interfaces follow PCI devices.
        def hardware_order(dev):
            info = info_map[dev]
            if not info['pci_chain']:
                return (2, 0, dev)
            numa = info.get('numa_node')
            return (0, int(numa), dev) if numa and numa.isdigit() else (1, 0, dev)

        for dev in sorted(devs, key=hardware_order):
            info = info_map[dev]
            chain = info['pci_chain']
            if not chain:
                group = tree_child(root, ('non-pci',), 'Non-PCI interfaces (virtual, USB or other)')
                tree_child(group, ('iface',dev), nic_description(info))
                continue
            group = numa_group(root,info,system)
            domain = chain[0]['pci'].split(':',1)[0]
            branch = tree_child(group,('pci-domain',domain),f'PCI domain {domain}')
            for node in chain:
                key = ('pci', node['pci'])
                if key not in branch['children']:
                    tree_child(branch, key, pci_description(node))
                branch = branch['children'][key]
            tree_child(branch,('iface',dev),nic_description(info))
    elif view == 'network':
        for dev in devs:
            d = details[dev]
            branch = tree_child(root,('iface',dev),nic_description(info_map[dev]))
            relations = [('Master',d['master']),('Upper interfaces',d['uppers']),
                         ('Lower interfaces',d['lowers'])]
            for title, values in relations:
                if values:
                    group = tree_child(branch,('relation',title),title)
                    for item in ([values] if isinstance(values,str) else values):
                        tree_child(group,('iface',item),item)
            if not branch['children']:
                tree_child(branch,('standalone',), 'No known upper/lower/master interfaces')
    elif view == 'cpu':
        for dev in devs:
            info = info_map[dev]
            group = numa_group(root,info,system)
            branch = tree_child(group,('iface',dev),nic_description(info))
            irqs = details[dev]['irqs']
            if not irqs:
                tree_child(branch,('unknown',), 'IRQ mapping unavailable')
            for irq in irqs:
                hint = irq['channel_index_hint']
                bits = [f'IRQ {irq["irq"]}']
                if hint is not None:
                    bits.append(f'channel hint {hint}')
                bits.append(f'effective CPUs {irq["effective_affinity"] or "unknown"}')
                tree_child(branch,('irq',irq['irq']), ' — '.join(bits))
    else:  # datapath
        for dev in devs:
            info = info_map[dev]
            d = details[dev]
            group = numa_group(root,info,system)
            branch = tree_child(group,('iface',dev),nic_description(info))
            rss = d['rss']
            if rss is not None:
                counts = {q:rss.count(q) for q in sorted(set(rss))}
                tree_child(branch,('rss',),f'RSS indirection [{len(rss)} entries, queue weights {counts}]')
            else:
                tree_child(branch,('rss',),'RSS indirection unavailable')
            rx = d['rx_queues']
            tx = d['tx_queues']
            tree_child(branch,('rx',),f'RX queues {cpulist(rx) if rx else "unavailable"}')
            tree_child(branch,('tx',),f'TX queues {cpulist(tx) if tx else "unavailable"}')
            irq_branch = tree_child(branch,('irqs',), 'IRQ vectors (queue labels are hints, not proven NAPI mapping)')
            for irq in d['irqs']:
                hint = irq['channel_index_hint']
                tree_child(irq_branch,('irq',irq['irq']),
                           f'IRQ {irq["irq"]} — channel hint {hint if hint is not None else "?"} '
                           f'— effective CPUs {irq["effective_affinity"] or "unknown"}')
            if not d['irqs']:
                tree_child(irq_branch,('unavailable',), 'No attributable IRQ vectors')
            if d['xdp']:
                tree_child(branch,('xdp',),f'XDP {d["xdp"]}')
    return root


def display_topology(system, args):
    if getattr(args, 'json', False):
        if args.format not in ('text', 'json'):
            raise DoctorError('--json and --format dot cannot be combined')
        args.format = 'json'
    devs = [args.device] if args.device else system.devices()
    data = {}
    info_map = {}
    for dev in devs:
        i = system.if_info(dev)
        info_map[dev] = i
        if args.view == 'network':
            data[dev] = system.network([dev])[dev]
        elif args.view == 'cpu':
            data[dev] = {'numa': i['numa_node'], 'local_cpus': i['local_cpus'], 'irqs': system.iface_irqs(dev)}
        elif args.view == 'datapath':
            data[dev] = {'pci': i['pci'], 'numa': i['numa_node'], 'rx_queues': i['rx_queues'],
                         'tx_queues': i['tx_queues'], 'irqs': system.iface_irqs(dev),
                         'rss': system.rss(dev), 'xdp': i['xdp'],
                         'note': 'IRQ channel indices are hints from interrupt labels, not independently proven NAPI mappings.'}
        else:
            data[dev] = {'pci': i['pci'], 'driver': i['driver'], 'numa': i['numa_node'],
                         'local_cpus': i['local_cpus'], 'rx_queues': len(i['rx_queues']),
                         'tx_queues': len(i['tx_queues']), 'channels': i['channels'],
                         'pci_chain': i['pci_chain']}
    if args.format == 'json':
        out_json({'view': args.view, 'devices': data})
    elif args.format == 'dot':
        print('digraph nic_doctor {\n  rankdir=LR;\n  node [shape=box];')
        for dev in devs:
            d = data[dev]
            safe = lambda s: str(s).replace('\\', '\\\\').replace('"', '\\"')
            iface = 'dev_'+re.sub(r'[^A-Za-z0-9_]', '_', dev)
            print(f'  {iface} [label="{safe(dev)}"];')
            if args.view == 'network':
                for lower in d['lowers']:
                    print(f'  "{safe(lower)}" -> {iface};')
                for upper in d['uppers']:
                    print(f'  {iface} -> "{safe(upper)}";')
            else:
                if d.get('pci') and not (args.view == 'hardware' and d.get('pci_chain')):
                    print(f'  "{safe(d["pci"])}" -> {iface};')
                if args.view == 'hardware' and d.get('pci_chain'):
                    chain = d['pci_chain']
                    if d.get('numa') not in (None, '-1'):
                        print(f'  "NUMA {safe(d["numa"])}" -> "{safe(chain[0]["pci"])}";')
                    for parent, child in zip(chain,chain[1:]):
                        print(f'  "{safe(parent["pci"])}" -> "{safe(child["pci"])}";')
                    print(f'  "{safe(chain[-1]["pci"])}" -> {iface};')
                if args.view in ('cpu', 'datapath'):
                    for irq in d['irqs']:
                        dest = f'irq_{irq["irq"]}'
                        print(f'  {iface} -> {dest};')
                        print(f'  {dest} [label="IRQ {irq["irq"]} ({safe(irq["name"])})"];')
                        for cpu in parse_cpulist(irq['effective_affinity']) if irq['effective_affinity'] else []:
                            print(f'  {dest} -> cpu_{cpu};\n  cpu_{cpu} [label="CPU {cpu}"];')
        print('}')
    else:
        unique_pci = {i['pci'] for i in info_map.values() if i['pci']}
        print('NIC Doctor  |  TOPOLOGY')
        print(f'Interfaces {len(devs)}  |  PCI functions {len(unique_pci)}')
        print()
        print({'hardware':'HARDWARE TREE', 'network':'NETWORK TREE',
               'cpu':'CPU / IRQ TREE', 'datapath':'DATAPATH TREE'}[args.view])
        for line in tree_lines(topology_tree(system,devs,args.view,info_map,data)):
            print(line)
        if not devs:
            print('  (no interfaces discovered)')
        if args.view == 'datapath':
            print('Note: IRQ labels do not establish a verified queue ↔ NAPI ↔ IRQ mapping.')
