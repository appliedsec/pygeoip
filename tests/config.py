import os.path

_data_dir = "/Users/jennifere/projects/pygeoip/data"

COUNTRY_DB_PATH = os.path.join(os.path.abspath(_data_dir), 'GeoIP.dat')
ISP_DB_PATH = os.path.join(os.path.abspath(_data_dir), 'GeoIPISP.dat')
ORG_DB_PATH = os.path.join(os.path.abspath(_data_dir), 'GeoIPOrg.dat')
CITY_DB_PATH = os.path.join(os.path.abspath(_data_dir), 'GeoLiteCity.dat')
REGION_DB_PATH = os.path.join(os.path.abspath(_data_dir), 'GeoIPRegion-515.dat')
