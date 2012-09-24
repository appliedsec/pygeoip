import os.path as path

DATA_DIR = path.join(path.dirname(path.realpath(__file__)), 'data')

COUNTRY_DB_PATH = path.join(DATA_DIR, 'GeoIP.dat')
REGION_DB_PATH = path.join(DATA_DIR, 'GeoIPRegion.dat')
CITY_DB_PATH = path.join(DATA_DIR, 'GeoLiteCity.dat')
ORG_DB_PATH = path.join(DATA_DIR, 'GeoIPOrg.dat')
