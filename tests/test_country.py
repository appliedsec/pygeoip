# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

import pygeoip
from tests.config import COUNTRY_DB_PATH, COUNTRY_V6_DB_PATH


class TestGeoIPCountryFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)
        self.gi6 = pygeoip.GeoIP(COUNTRY_V6_DB_PATH)

    def testCountryCodeByAddr(self):
        us_code = self.gi.country_code_by_addr('64.17.254.216')
        it_code = self.gi.country_code_by_addr('78.26.70.208')
        jp6_code = self.gi6.country_code_by_addr('2001:200::')

        self.assertEqual(us_code, 'US')
        self.assertEqual(it_code, 'IT')
        self.assertEqual(jp6_code, 'JP')

    def testCountryNameByAddr(self):
        us_name = self.gi.country_name_by_addr('64.17.254.216')
        it_name = self.gi.country_name_by_addr('78.26.70.208')
        jp6_name = self.gi6.country_name_by_addr('2001:200::')

        self.assertEqual(us_name, 'United States')
        self.assertEqual(it_name, 'Italy')
        self.assertEqual(jp6_name, 'Japan')

    @raises(pygeoip.GeoIPError)
    def testOpen4With6(self):
        data = self.gi.country_code_by_addr('2001:200::')
        raise ValueError(data)

    @raises(pygeoip.GeoIPError)
    def testOpen6With4(self):
        data = self.gi6.country_code_by_addr('78.26.70.208')
        raise ValueError(data)

    @raises(pygeoip.GeoIPError)
    def testOrgByAddr(self):
        self.gi.org_by_addr('78.26.70.208')

    @raises(pygeoip.GeoIPError)
    def testRecordByAddr(self):
        self.gi.record_by_addr('78.26.70.208')

    @raises(pygeoip.GeoIPError)
    def testRegionByAddr(self):
        self.gi.region_by_addr('78.26.70.208')

    @raises(pygeoip.GeoIPError)
    def testTimeZoneByAddr(self):
        self.gi.time_zone_by_addr('78.26.70.208')
