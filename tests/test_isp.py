# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import ISP_DB_PATH


class TestGeOIPISPFunctions(unittest.TestCase):
    def setUp(self):
        self.us_isp = 'Turner Broadcasting System'
        self.us_ip = '157.166.255.18'
        self.us_hostname = 'cnn.com'

        self.se_isp = 'IP-Only Tele Communication AB'
        self.se_ip = '213.132.112.97'
        self.se_hostname = 'blocket.se'

        self.gi = pygeoip.GeoIP(ISP_DB_PATH)

    def testISPByAddr(self):
        se_isp = self.gi.org_by_addr(self.se_ip)
        us_isp = self.gi.org_by_addr(self.us_ip)

        self.assertEqual(se_isp, self.se_isp)
        self.assertEqual(us_isp, self.us_isp)

    def testISPByName(self):
        se_isp = self.gi.org_by_name(self.se_hostname)
        us_isp = self.gi.org_by_name(self.us_hostname)

        self.assertEqual(se_isp, self.se_isp)
        self.assertEqual(us_isp, self.us_isp)
