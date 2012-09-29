# -*- coding: utf-8 -*-
import unittest

import pygeoip
from pygeoip.const import PY2, PY3
from tests.config import CITY_DB_PATH


class TestGeoIPCacheMethods(unittest.TestCase):
    def setUp(self):
        self.de_hostname = 'www.osnabrueck.de'
        self.de_city = 'Osnabr\xfcck'.decode('latin1') if PY2 else 'Osnabrück'
        self.gic = pygeoip.GeoIP(CITY_DB_PATH)

    def testUnicodeCity(self):
        record = self.gic.record_by_name(self.de_hostname)
        self.assertEqual(type(record['city']), unicode if PY2 else str)
        self.assertEqual(record['city'], self.de_city)
