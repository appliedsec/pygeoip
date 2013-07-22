# -*- coding: utf-8 -*-
import unittest

import pygeoip
import pygeoip.timezone
from tests.config import CITY_DB_PATH


class TestGeoIPTimeZoneFunctions(unittest.TestCase):
    def setUp(self):
        self.us_hostname = 'google.com'
        self.us_ip = '64.233.161.99'

        self.gb_hostname = 'bbc.com'
        self.gb_ip = '212.58.253.68'

        self.gic = pygeoip.GeoIP(CITY_DB_PATH)

    def testTimeZoneInternals(self):
        tz = pygeoip.timezone.time_zone_by_country_and_region('XX')
        self.assertEquals(tz, None)

        tz = pygeoip.timezone.time_zone_by_country_and_region('US', 'NY')
        self.assertEquals(tz, 'America/New_York')

        tz = pygeoip.timezone.time_zone_by_country_and_region('US', 'XX')
        self.assertEquals(tz, None)

    def testTimeZoneByAddr(self):
        us_time_zone = self.gic.time_zone_by_addr(self.us_ip)
        gb_time_zone = self.gic.time_zone_by_addr(self.gb_ip)

        self.assertEquals(us_time_zone, 'America/Los_Angeles')
        self.assertEquals(gb_time_zone, 'Europe/London')

    def testTimeZoneByName(self):
        us_time_zone = self.gic.time_zone_by_name(self.us_hostname)
        gb_time_zone = self.gic.time_zone_by_name(self.gb_hostname)

        self.assertEquals(us_time_zone, 'America/Los_Angeles')
        self.assertEquals(gb_time_zone, 'Europe/London')
