# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import ORG_DB_PATH


class TestGeoIPOrgFunctions(unittest.TestCase):
    def setUp(self):
        self.us_org = 'APPLE COMPUTER'
        self.us_ip = '17.172.224.47'
        self.us_hostname = 'apple.com'

        self.gb_org = 'BBC'
        self.gb_ip = '212.58.253.68'
        self.gb_hostname = 'bbc.com'

        self.gio = pygeoip.GeoIP(ORG_DB_PATH)

    def testOrgByAddr(self):
        gb_org = self.gio.org_by_addr(self.gb_ip)
        us_org = self.gio.org_by_addr(self.us_ip)

        self.assertEqual(gb_org, self.gb_org)
        self.assertEqual(us_org, self.us_org)

    def testOrgByName(self):
        gb_org = self.gio.org_by_name(self.gb_hostname)
        us_org = self.gio.org_by_name(self.us_hostname)

        self.assertEqual(gb_org, self.gb_org)
        self.assertEqual(us_org, self.us_org)
