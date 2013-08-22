# -*- coding: utf-8 -*-
import unittest

import pygeoip
from pygeoip import const
from tests.config import COUNTRY_DB_PATH


class TestMemoryCache(unittest.TestCase):
    def testMemoryCache(self):
        gi = pygeoip.GeoIP(COUNTRY_DB_PATH, flags=const.MEMORY_CACHE, cache=False)
        self.assertEqual(gi._type, 'MEMORY_CACHE')

        code = gi.country_code_by_name('dn.se')
        self.assertEqual(code, 'SE')
