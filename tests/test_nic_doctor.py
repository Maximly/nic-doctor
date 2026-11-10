# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
import importlib.machinery
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['common.py', 'discovery.py', 'topology.py', 'tuning.py', 'cli.py']
n = type(sys)('nic_doctor')
n.__file__ = str(ROOT / 'nic-doctor.sh')
source = '\n'.join((ROOT / 'src' / name).read_text() for name in SOURCES)
exec(compile(source, n.__file__, 'exec'), n.__dict__)

CHANNELS='''Channel parameters for eth0:
Pre-set maximums:
RX: n/a
TX: n/a
Other: 0
Combined: 63
Current hardware settings:
RX: n/a
TX: n/a
Other: 0
Combined: 2
'''
RSS='''RX flow hash indirection table for eth0 with 4 RX ring(s):
    0: 0 1 0 1
    4: 0 1 0 1
RSS hash key: aaaaa
'''


class UnitTests(unittest.TestCase):
    def test_cpu_ranges_masks(self):
        self.assertEqual(n.parse_cpulist('8-10,12,9'), [8,9,10,12])
        self.assertEqual(n.cpulist([1,3,4,5,7]),'1,3-5,7')
        self.assertEqual(n.mask_cpus(n.cpu_mask([0,31,32,71])), [0,31,32,71])
        for bad in ['1-', '4-2', '0,foo', '', '0; touch /tmp/foo']:
            with self.assertRaises(n.DoctorError):n.parse_cpulist(bad)

    def test_ethtool_parsers(self):
        self.assertEqual(n.ethtool_channels(CHANNELS)['current']['combined'],2)
        self.assertEqual(n.ethtool_rss(RSS),[0,1,0,1,0,1,0,1])
        self.assertEqual(n.rss_equal_model([0,1,0,1]), {'start':0,'equal':2})
        self.assertEqual(n.rss_equal_model([3,4,3,4]), {'start':3,'equal':2})
        self.assertIsNone(n.rss_equal_model([0,1,1,0]))
        self.assertEqual(n.ethtool_stats(' rx_packets: 12\n rx_wqe_err: 0\n'),{'rx_packets':12,'rx_wqe_err':0})

    def test_diff(self):
        self.assertEqual(n.diff_dict({'timestamp_utc':'A','devices':{'a':1}}, {'timestamp_utc':'B','devices':{'a':2}}), [('devices.a',1,2)])


class LinuxFixture(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        self.sys=root/'sys';self.proc=root/'proc';self.state=root/'state'
        self.net=self.sys/'class/net/eth0';self.net.mkdir(parents=True)
        (self.sys/'devices/system/cpu').mkdir(parents=True)
        (self.sys/'devices/system/cpu/online').write_text('0-3\n')
        (self.sys/'devices/system/node/node0').mkdir(parents=True)
        (self.sys/'devices/system/node/node0/cpulist').write_text('0-3\n')
        pci=self.sys/'pci/0000:01:00.0';(pci/'msi_irqs').mkdir(parents=True)
        (pci/'msi_irqs/31').touch();(pci/'msi_irqs/32').touch();(pci/'msi_irqs/33').touch()
        (pci/'numa_node').write_text('0\n')
        (pci/'local_cpulist').write_text('0-3\n')
        (self.net/'device').symlink_to(pci)
        for name,value in [('ifindex','2'),('iflink','2'),('address','00:11:22:33:44:55'),('operstate','up'),('speed','100000'),('mtu','1500')]:
            (self.net/name).write_text(value+'\n')
        for i in range(2):
            for direction,key,initial in [('rx','rps_cpus','0'),('tx','xps_cpus','0')]:
                p=self.net/f'queues/{direction}-{i}';p.mkdir(parents=True)
                (p/key).write_text(initial+'\n')
        stats=self.net/'statistics';stats.mkdir()
        for name,val in [('rx_packets','1000'),('rx_bytes','64000'),('rx_dropped','10')]:
            (stats/name).write_text(val+'\n')
        self.proc.mkdir()
        (self.proc/'interrupts').write_text('''           CPU0 CPU1 CPU2 CPU3
 31:   10   0  0  0  PCI-MSI-edge eth0-0
 32:    0  10 0  0  PCI-MSI-edge eth0-1
 33:    0   1 0  0  PCI-MSI-edge mlx5_comp2@pci:0000:01:00.0
''')
        for irq,cpu in [(31,0),(32,1),(33,2)]:
            p=self.proc/f'irq/{irq}';p.mkdir(parents=True)
            (p/'smp_affinity_list').write_text(str(cpu)+'\n')
            (p/'effective_affinity_list').write_text(str(cpu)+'\n')
        self.sysobj=n.System(self.sys,self.proc,self.state)
        orig_run=n.run
        def fake_run(*args,**kwargs):
            if args[:2] == ('ethtool','-l'):return CHANNELS
            if args[:2] == ('ethtool','-x'):return RSS
            if args[:2] == ('ethtool','-i'):return 'driver: mlx5_core\nfirmware-version: 20.1\n'
            if args[:2] == ('ethtool','-S'):return ' rx_out_of_buffer: 22\n'
            return None
        self.patch=mock.patch.object(n,'run',side_effect=fake_run)
        self.patch.start();self.addCleanup(self.patch.stop)

    def test_cli_help_show_all_and_glob(self):
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.assertEqual(n.main(['help'], self.sysobj), 0)
        self.assertIn('nic-doctor', capture.getvalue())

        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.assertEqual(n.main(['help', 'show'], self.sysobj), 0)
        self.assertIn('DEVICE', capture.getvalue())

        for args in (['show'], ['show', 'all'], ['show', '*'],
                     ['show', 'eth*'], ['show', 'eth0']):
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                self.assertEqual(n.main(args, self.sysobj), 0)
            self.assertIn('DEVICE eth0', capture.getvalue())

        for args in (['show', '--json'], ['show', '*', '--json'], ['show', 'eth0', '--json']):
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                self.assertEqual(n.main(args, self.sysobj), 0)
            data = json.loads(capture.getvalue())
            info = data[0] if isinstance(data, list) else data
            self.assertEqual(info['device'], 'eth0')

        with self.assertRaisesRegex(n.DoctorError, "Shell expanded"):
            n.main(['show', 'README.md', 'Makefile'], self.sysobj)


    def test_parameterless_help_and_json_topology_alias(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(n.main([], self.sysobj), 0)
        self.assertIn('usage: nic-doctor', output.getvalue())
        self.assertIn('topology', output.getvalue())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(n.main(['topology', '--json'], self.sysobj), 0)
        self.assertIn('eth0', json.loads(output.getvalue())['devices'])
        with self.assertRaisesRegex(n.DoctorError, 'cannot be combined'):
            n.main(['topology', '--json', '--format', 'dot'], self.sysobj)
    def test_discovery(self):
        i=self.sysobj.if_info('eth0')
        self.assertEqual(i['pci'],'0000:01:00.0')
        self.assertEqual(i['driver'],'mlx5_core')
        self.assertEqual(i['rx_queues'],[0,1])
        self.assertEqual(self.sysobj.active_irqs('eth0')[0]['irq'],31)
        self.assertEqual(len(self.sysobj.iface_irqs('eth0')),3)
        self.assertEqual(self.sysobj.rss('eth0'),[0,1]*4)

    def test_topology_shared_hardware_tree(self):
        # Multiple netdevs share their PCI ancestors.
        pci_root=self.sys/'devices/pci0000:80'
        bridge=pci_root/'0000:80:01.0'
        bridge.mkdir(parents=True)
        for name,value in [('class','0x060400'),('current_link_speed','16.0 GT/s PCIe'),
                           ('current_link_width','16'),('max_link_speed','32.0 GT/s PCIe'),
                           ('max_link_width','16')]:
            (bridge/name).write_text(value+'\n')
        for idx,dev in [(0,'eth1'),(0,'eth2'),(1,'eth3')]:
            endpoint=bridge/f'0000:81:00.{idx}'
            endpoint.mkdir(exist_ok=True)
            (endpoint/'class').write_text('0x020000\n')
            (endpoint/'numa_node').write_text('0\n')
            (endpoint/'local_cpulist').write_text('0-3\n')
            (endpoint/'current_link_speed').write_text('16.0 GT/s PCIe\n')
            (endpoint/'current_link_width').write_text('8\n')
            iface=self.sys/f'class/net/{dev}'
            iface.mkdir(parents=True)
            (iface/'device').symlink_to(endpoint)
            (iface/'operstate').write_text('up\n')
            (iface/'speed').write_text('100000\n')
            (iface/'ifindex').write_text(str(10+len(dev))+'\n')
            (iface/'iflink').write_text(str(10+len(dev))+'\n')
        loop=self.sys/'class/net/lo'
        loop.mkdir(parents=True)
        (loop/'ifindex').write_text('1\n')
        (loop/'operstate').write_text('unknown\n')
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            self.assertEqual(n.main(['topology'],self.sysobj),0)
        output=captured.getvalue()
        self.assertIn('NIC Doctor  |  TOPOLOGY',output)
        self.assertIn('HARDWARE TREE\nNetwork\n',output)
        self.assertIn('NUMA node 0 [local CPUs 0-3]',output)
        self.assertIn('PCI domain 0000',output)
        self.assertEqual(output.count('80:01.0 — PCIe bridge'),1)
        self.assertIn('Gen4 x16 (max Gen5 x16)',output)
        self.assertEqual(output.count('81:00.0 — Network controller'),1)
        self.assertEqual(output.count('81:00.1 — Network controller'),1)
        self.assertIn('eth1 [',output)
        self.assertIn('eth2 [',output)
        self.assertIn('eth3 [',output)
        self.assertIn('Non-PCI interfaces',output)
        self.assertIn('└─ lo [',output)
        self.assertIn('│',output)
        # Selecting one device preserves its PCI ancestry.
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            n.main(['topology','--device','eth2'],self.sysobj)
        isolated=captured.getvalue()
        self.assertIn('80:01.0',isolated)
        self.assertIn('eth2 [',isolated)
        self.assertNotIn('eth1 [',isolated)
        # JSON output is independent of terminal formatting.
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            n.main(['topology','--device','eth2','--format','json'],self.sysobj)
        value=json.loads(captured.getvalue())
        self.assertEqual([x['pci'] for x in value['devices']['eth2']['pci_chain']],
                         ['0000:80:01.0','0000:81:00.0'])
        self.assertEqual(value['devices']['eth2']['pci_chain'][0]['pcie_max_width'],'16')

    def test_topology_other_views_are_trees(self):
        for view,title in [('network','NETWORK TREE'),('cpu','CPU / IRQ TREE'),
                           ('datapath','DATAPATH TREE')]:
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                n.main(['topology','--view',view],self.sysobj)
            value=captured.getvalue()
            self.assertIn(title+'\nNetwork\n',value)
            self.assertIn('eth0 [',value)
            self.assertIn('└─',value)
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            n.main(['topology','--view','cpu','--device','eth0'],self.sysobj)
        self.assertIn('IRQ 31 — channel hint 0 — effective CPUs 0',captured.getvalue())

    def test_pin_plan_and_validation(self):
        steps=n.pin_actions(self.sysobj,'eth0',[2,3])
        self.assertEqual([x['after'] for x in steps],['2','3'])
        with self.assertRaises(n.DoctorError):n.pin_actions(self.sysobj,'eth0',[3])
        with self.assertRaises(n.DoctorError):n.pin_actions(self.sysobj,'eth0',[4,5])
        with self.assertRaises(n.DoctorError):n.pin_actions(self.sysobj,'eth0',[0,1], '31-33')

    def test_mutation_transaction_and_rollback(self):
        acts=n.queue_actions(self.sysobj,'eth0',[2,3],'tx','xps_cpus')
        self.assertEqual(len(acts),2)
        with mock.patch.object(n,'require_root'):
            ident=n.transaction(self.sysobj,acts,'test xps')
            self.assertEqual(n.mask_cpus(n.read(self.net/'queues/tx-0/xps_cpus')),[2])
            self.assertEqual(n.mask_cpus(n.read(self.net/'queues/tx-1/xps_cpus')),[3])
            n.roll_back(self.sysobj,ident)
        self.assertEqual(n.mask_cpus(n.read(self.net/'queues/tx-0/xps_cpus')),[])
        self.assertEqual(n.mask_cpus(n.read(self.net/'queues/tx-1/xps_cpus')),[])

    def test_ambiguous_irq_rejected(self):
        (self.proc/'interrupts').write_text(' 31: 1 0 PCI-MSI-edge mlx5_comp0@pci:0000:01:00.0\n')
        with self.assertRaisesRegex(n.DoctorError,'cannot prove IRQ'):
            n.pin_actions(self.sysobj,'eth0',[0,1])

    def test_profile_and_diagnose(self):
        profile={'devices':{'eth0':{'channels':{'combined':2},'rps':{'enabled':False},'xps':{'cpus':'2-3'}}}}
        actions=n.profile_actions(self.sysobj,'eth0',profile['devices']['eth0'])
        self.assertTrue(any(x['kind']=='file' for x in actions))
        self.assertFalse(any(x['kind']=='channels' for x in actions))
        diag=n.diagnose(self.sysobj,'eth0',0)
        self.assertTrue(any('Receiver-only' in x for x in diag['limits']))


if __name__ == '__main__': unittest.main()
