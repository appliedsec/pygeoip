# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import REGION_DB_PATH


class TestGeoIPRegionFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(REGION_DB_PATH)

    def testRegionByAddr(self):
        region_name = self.gi.region_by_addr('17.172.224.47')
        self.assertEqual(region_name, {
            'region_code': 'CA',
            'country_code': 'US'
        })

    def testCountryCodeByAddr(self):
        us_code = self.gi.country_code_by_addr('17.172.224.47')
        self.assertEqual(us_code, 'US')
