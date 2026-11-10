# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
"""Checks and optimization plans using a synthetic sysfs/procfs fixture."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['common.py', 'discovery.py', 'topology.py', 'tuning.py', 'analysis.py', 'cli.py']
module = type(sys)('nic_doctor_analysis_fixture')
module.__file__ = str(ROOT/'nic-doctor.sh')
exec(compile('\n'.join((ROOT/'src'/x).read_text() for x in NAMES), module.__file__, 'exec'), module.__dict__)
n = module

CHANS = '''Pre-set maximums:
RX: n/a
TX: n/a
Other: 0
Combined: 8
Current hardware settings:
RX: n/a
TX: n/a
Other: 0
Combined: 2
'''
RSS = '''RX flow hash indirection table for eth0 with 2 RX ring(s):
  0: 0 1 0 1
'''

class AnalysisFixture(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root=Path(temporary.name)
        self.sys=root/'sys'
        self.proc=root/'proc'
        self.dev=self.sys/'class/net/eth0'
        self.dev.mkdir(parents=True)
        pci=self.sys/'devices/pci0000:00/0000:01:00.0'
        (pci/'msi_irqs').mkdir(parents=True)
        for irq in (70,71):
            (pci/'msi_irqs'/str(irq)).touch()
        for key,value in [('numa_node','0'),('local_cpulist','0-3'),
                          ('current_link_speed','16.0 GT/s PCIe'),('max_link_speed','16.0 GT/s PCIe'),
                          ('current_link_width','16'),('max_link_width','16')]:
            (pci/key).write_text(value)
        (self.dev/'device').symlink_to(pci)
        for key,value in [('ifindex','2'),('iflink','2'),('operstate','up'),('speed','100000'),('mtu','1500')]:
            (self.dev/key).write_text(value)
        for i in range(2):
            for direction in ('rx','tx'):
                (self.dev/f'queues/{direction}-{i}').mkdir(parents=True)
        for key,value in [('rx_packets','100000'),('tx_packets','120000'),('rx_bytes','6400000'),
                          ('tx_bytes','7680000'),('rx_dropped','0')]:
            stats=self.dev/'statistics';stats.mkdir(exist_ok=True)
            (stats/key).write_text(value)
        self.proc.mkdir()
        (self.proc/'interrupts').write_text('''           CPU0 CPU1 CPU2 CPU3
 70:  20 0 0 0 PCI-MSI-edge eth0-0
 71:  0 0 20 0 PCI-MSI-edge eth0-1
''')
        for irq,cpu in [(70,0),(71,2)]:
            directory=self.proc/f'irq/{irq}'
            directory.mkdir(parents=True)
            (directory/'smp_affinity_list').write_text(str(cpu))
            (directory/'effective_affinity_list').write_text(str(cpu))
        (self.sys/'devices/system/cpu').mkdir(parents=True)
        (self.sys/'devices/system/cpu/online').write_text('0-3')
        (self.sys/'devices/system/node/node0').mkdir(parents=True)
        (self.sys/'devices/system/node/node0/cpulist').write_text('0-3')
        # 0/2 and 1/3 are SMT sibling pairs.
        for cpu in range(4):
            topo=self.sys/f'devices/system/cpu/cpu{cpu}/topology'
            topo.mkdir(parents=True)
            (topo/'physical_package_id').write_text('0')
            (topo/'core_id').write_text(str(cpu%2))
            (topo/'thread_siblings_list').write_text('0,2' if cpu%2==0 else '1,3')
        self.host=n.System(self.sys,self.proc,root/'state')
        self.vendor_count=0
        def fake_run(*args, **kw):
            if args[:2]==('ethtool','-i'): return 'driver: mlx5_core\n'
            if args[:2]==('ethtool','-l'): return CHANS
            if args[:2]==('ethtool','-x'): return RSS
            if args[:2]==('ethtool','-S'):
                self.vendor_count+=1
                return 'rx_out_of_buffer: '+str(10+(7 if self.vendor_count>=2 else 0))
            return None
        patch=mock.patch.object(n,'run',side_effect=fake_run)
        patch.start()
        self.addCleanup(patch.stop)
        patch=mock.patch.object(n,'irqbalance_active',return_value=False)
        patch.start();self.addCleanup(patch.stop)

    def test_status_is_instantaneous(self):
        out=n.status_report(self.host)
        self.assertEqual(len(out['interfaces']),1)
        self.assertEqual(out['interfaces'][0]['device'],'eth0')
        self.assertIn('Instantaneous',out['note'])
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.assertEqual(n.main(['status'], self.host),0)
        self.assertIn('Next: nic-doctor check',capture.getvalue())
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.assertEqual(n.main(['status','--json'], self.host),0)
        self.assertEqual(json.loads(capture.getvalue())['interfaces'][0]['device'],'eth0')

    def test_check_rate_and_buffer_exhaustion(self):
        with mock.patch.object(n.time, 'sleep', return_value=None), mock.patch.object(n.time,'monotonic',side_effect=[1.0,3.0]):
            data=n.check_report(self.host,'eth0',duration=1.0,focus='loss')
        self.assertEqual(data['sample_seconds'],2.0)
        self.assertEqual(data['rates']['eth0']['rx_mpps'],0)
        self.assertEqual([f['code'] for f in data['findings']],['rx.out_of_buffer'])
        self.assertEqual(data['findings'][0]['severity'],'warning')
        self.assertIn('out_of_buffer',data['findings'][0]['evidence'])
        self.assertEqual(data['findings'][0]['confidence'],'high')

    def test_core_conflict_and_optimized_selection(self):
        data=n.check_report(self.host,'eth0',duration=0,focus='placement')
        self.assertTrue(any(f['code']=='irq.shared_core' for f in data['findings']))
        plan=n.optimize_report(self.host,'eth0')
        self.assertEqual(plan['plans'][0]['status'],'planned')
        self.assertEqual(plan['plans'][0]['selected_cpus'],[0,1])
        self.assertEqual(len(plan['plans'][0]['changes']),1)
        self.assertEqual(plan['plans'][0]['changes'][0]['path'],str(self.proc/'irq/71/smp_affinity_list'))

    def test_optimizer_blocks_unproven_irq_map_and_smt_exhaustion(self):
        plan=n.optimize_report(self.host,'eth0',avoid_cpus=[0,2])
        self.assertEqual(plan['plans'][0]['status'],'blocked')
        self.assertIn('physical cores',plan['plans'][0]['error'])
        plan=n.optimize_report(self.host,'eth0',avoid_cpus=[0,2],allow_smt=True)
        self.assertEqual(plan['plans'][0]['selected_cpus'],[1,3])
        self.assertTrue(plan['plans'][0]['warnings'])
        (self.proc/'interrupts').write_text(''' CPU0 CPU1 CPU2 CPU3
 70: 0 1 0 0 PCI-MSI-edge mlx5_comp0
 71: 0 1 0 0 PCI-MSI-edge mlx5_comp1
''')
        blocked=n.optimize_report(self.host,'eth0')
        self.assertEqual(blocked['plans'][0]['status'],'blocked')
        self.assertIn('cannot prove',blocked['plans'][0]['error'])

    def test_explicit_selection_and_profile_output(self):
        dest=self.sys/'profile.json'
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(n.main(['optimize','eth0','--cpus','1,3','--profile-out',str(dest)],self.host),0)
        profile=json.loads(dest.read_text())
        self.assertEqual(profile['devices']['eth0']['irq']['cpus'],'1,3')
        self.assertEqual(n.profile_load(dest),profile)
        self.assertIn('Proposed IRQ CPUs',output.getvalue())

    def test_focus_strict_and_unknowns(self):
        irq_path=self.proc/'irq/70/effective_affinity_list'
        irq_path.write_text('7')
        data=n.check_report(self.host,'eth0',duration=0,focus='placement')
        self.assertTrue(any(f['code']=='irq.remote_numa' for f in data['findings']))
        self.assertFalse(any(f['code'].startswith('rx.') for f in data['findings']))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(n.main(['check','eth0','--focus','placement','--duration','0','--strict'],self.host),2)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(n.main(['check','eth0','--focus','loss','--duration','0','--strict'],self.host),0)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(n.main(['optimize','eth0','--avoid-cpus','0,2'],self.host),2)

    def test_explain_limits(self):
        report=n.explain_report(self.host,'eth0')
        self.assertEqual(len(report['queue_irq_labels']),2)
        self.assertEqual(report['rss_weights'],{0:2,1:2})
        self.assertTrue(any('not independently' in s for s in report['limitations']))
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.assertEqual(n.main(['explain','eth0'],self.host),0)
        self.assertIn('DATAPATH',capture.getvalue())

if __name__=='__main__':
    unittest.main()
