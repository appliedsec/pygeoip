# -*- coding: utf-8 -*-
import unittest

import pygeoip
from pygeoip import const
from tests.config import COUNTRY_DB_PATH

class TestMmapCache(unittest.TestCase):
    def testMmapCache(self):
        gi = pygeoip.GeoIP(COUNTRY_DB_PATH, flags=const.MMAP_CACHE, cache=False)
        self.assertEqual(gi._type, 'MMAP_CACHE')
