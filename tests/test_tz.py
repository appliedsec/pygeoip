# -*- coding: utf-8 -*-
import unittest

import pygeoip
import pygeoip.timezone
from tests.config import CITY_DB_PATH


class TestGeoIPTimeZoneFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(CITY_DB_PATH)

    def testTimeZoneInternals(self):
        tz = pygeoip.timezone.time_zone_by_country_and_region('XX')
        self.assertEquals(tz, None)

        tz = pygeoip.timezone.time_zone_by_country_and_region('US', 'NY')
        self.assertEquals(tz, 'America/New_York')

        tz = pygeoip.timezone.time_zone_by_country_and_region('US', 'XX')
        self.assertEquals(tz, None)

    def testTimeZoneByAddr(self):
        tz = self.gi.time_zone_by_addr('64.17.254.216')
        self.assertEquals(tz, 'America/Los_Angeles')
