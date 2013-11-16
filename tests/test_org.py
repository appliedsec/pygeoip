# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import ORG_DB_PATH


class TestGeoIPOrgFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(ORG_DB_PATH)

    def testOrgByAddr(self):
        org = self.gi.org_by_addr('70.46.123.145')
        self.assertEqual(org, 'DSLAM WAN Allocation')
