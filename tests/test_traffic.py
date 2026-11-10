# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
"""Traffic accounting source selection and rate reporting."""
import contextlib
import io
import unittest
from unittest import mock

from test_analysis import n


class FakeSystem:
    def __init__(self, before, after):
        self.samples = [before, after]

    def device(self, dev):
        if dev != 'eth0':
            raise n.DoctorError('unknown interface')

    def if_info(self, dev):
        return {'pci':None, 'operstate':'up','pci_chain':[], 'channels':None,
                'numa_node':'-1'}

    def iface_irqs(self, dev):
        return []

    def rss(self, dev):
        return None

    def counters(self, dev, vendor=False):
        return self.samples.pop(0)


class TrafficSourceTests(unittest.TestCase):
    def sample(self, before, after, traffic_source='auto'):
        host = FakeSystem(before, after)
        with mock.patch.object(n.time, 'sleep', return_value=None), \
             mock.patch.object(n.time, 'monotonic',side_effect=[100.0,105.0]):
            return n.check_report(host,'eth0',duration=5,focus='loss',traffic_source=traffic_source)

    def test_phy_preferred_when_xdp_traffic_bypasses_netdev(self):
        before = {'rx_packets':10, 'tx_packets':10, 'rx_bytes':600,
                  'tx_bytes':600, 'ethtool/rx_packets_phy':5_000_000,
                  'ethtool/tx_packets_phy':3_000_000,
                  'ethtool/rx_bytes_phy':300_000_000,
                  'ethtool/tx_bytes_phy':180_000_000}
        after = dict(before)
        after.update({'ethtool/rx_packets_phy':105_000_000,
                      'ethtool/tx_packets_phy':53_000_000,
                      'ethtool/rx_bytes_phy':6_300_000_000,
                      'ethtool/tx_bytes_phy':3_180_000_000})
        report=self.sample(before,after)
        rates=report['rates']['eth0']
        self.assertEqual(rates['rx_pps'],20_000_000)
        self.assertEqual(rates['tx_pps'],10_000_000)
        self.assertEqual(rates['rx_gbps'],9.6)
        self.assertEqual(rates['rx_source'],'PHY (port)')
        self.assertIn('traffic.accounting_domains',[f['code'] for f in report['findings']])
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            n.print_findings(report)
        self.assertIn('20.000 Mpps',out.getvalue())
        self.assertIn('PHY (port)',out.getvalue())

    def test_explicit_netdev_remains_available(self):
        before={'rx_packets':1,'rx_bytes':64,'ethtool/rx_packets_phy':10,
                'ethtool/rx_bytes_phy':640}
        after={'rx_packets':1,'rx_bytes':64,'ethtool/rx_packets_phy':5_000_010,
               'ethtool/rx_bytes_phy':320_000_640}
        report=self.sample(before,after,'netdev')
        self.assertEqual(report['rates']['eth0']['rx_pps'],0)
        self.assertEqual(report['rates']['eth0']['rx_source'],'netdev (host)')

    def test_vport_fallback_requires_complete_categories(self):
        before={}
        after={}
        for d in ('rx','tx'):
            for kind in ('unicast','multicast','broadcast'):
                key='ethtool/'+d+'_vport_'+kind+'_packets'
                bytes_key='ethtool/'+d+'_vport_'+kind+'_bytes'
                before[key]=100
                after[key]=200
                before[bytes_key]=6400
                after[bytes_key]=12800
        rates=self.sample(before,after)['rates']['eth0']
        self.assertEqual(rates['rx_source'],'vPort (PF)')
        self.assertEqual(rates['rx_pps'],60)
        del after['ethtool/rx_vport_broadcast_packets']
        rates=self.sample(before,after)['rates']['eth0']
        self.assertIsNone(rates['rx_source'])
        self.assertEqual(rates['tx_source'],'vPort (PF)')

    def test_netdev_fallback_for_generic_nic(self):
        before={'rx_packets':100,'tx_packets':20,'rx_bytes':6400,'tx_bytes':1280}
        after={'rx_packets':225,'tx_packets':45,'rx_bytes':14400,'tx_bytes':2880}
        rates=self.sample(before,after)['rates']['eth0']
        self.assertEqual(rates['rx_source'],'netdev (host)')
        self.assertEqual(rates['rx_pps'],25)
        self.assertEqual(n.human_rate(rates['rx_pps'],'pps'),'25.00 pps')

    def test_missing_counters_not_reported_as_zero(self):
        rates=n.traffic_rates({},5)
        self.assertIsNone(rates['rx_pps'])
        self.assertIsNone(rates['tx_pps'])
        self.assertEqual(n.human_rate(rates['rx_pps'],'pps'),'-')

    def test_small_nonzero_rate_is_not_rounded_to_zero(self):
        self.assertEqual(n.human_rate(10,'pps'),'10.00 pps')
        self.assertEqual(n.human_rate(2500,'pps'),'2.500 kpps')
        self.assertEqual(n.human_rate(25_000_000,'pps'),'25.000 Mpps')

    def test_unknown_source_rejected(self):
        with self.assertRaises(n.DoctorError):
            n.traffic_rates({},5,'unknown')


if __name__=='__main__':
    unittest.main()
