# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import NETSPEED_DB_PATH, NETSPEEDCELL_DB_PATH


class TestGeoIPNetspeedFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(NETSPEED_DB_PATH)

    def testNetSpeedByAddr(self):
        netspeed = self.gi.id_by_addr('17.172.224.47')
        self.assertEqual(netspeed, 3)

    def testNetSpeedByAddrWrapper(self):
        netspeed = self.gi.netspeed_by_addr('17.172.224.47')
        self.assertEqual(netspeed, 'Corporate')
