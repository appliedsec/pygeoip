# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import NETSPEED_DB_PATH


class TestGeoIPOrgFunctions(unittest.TestCase):
    def setUp(self):
        self.ip = '17.172.224.47'
        self.hostname = 'apple.com'
        self.gi = pygeoip.GeoIP(NETSPEED_DB_PATH)

    def testNetSpeedByAddr(self):
        netspeed = self.gi.id_by_addr(self.ip)
        self.assertEqual(netspeed, 3)

    def testNetSpeedByAddrWrapper(self):
        netspeed = self.gi.netspeed_by_addr(self.ip)
        self.assertEqual(netspeed, 'Corporate')

    def testNetSpeedByNameWrapper(self):
        netspeed = self.gi.netspeed_by_name(self.hostname)
        self.assertEqual(netspeed, 'Corporate')
