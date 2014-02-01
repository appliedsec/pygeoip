# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import ISP_DB_PATH


class TestGeOIPISPFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(ISP_DB_PATH)

    def testISPByAddr(self):
        isp = self.gi.isp_by_addr('70.46.123.145')
        self.assertEqual(isp, 'FDN Communications')
