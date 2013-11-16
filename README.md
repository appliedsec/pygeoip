# Pure Python GeoIP API

This library is based on [Maxmind's GeoIP C API](https://github.com/maxmind/geoip-api-c).

Tested with Python version 2.5, 2.6, 2.7, 3.2 and 3.3.

[![Build Status](https://api.travis-ci.org/appliedsec/pygeoip.png?branch=master)](https://travis-ci.org/appliedsec/pygeoip) [![Coverage Status](https://coveralls.io/repos/appliedsec/pygeoip/badge.png)](https://coveralls.io/r/appliedsec/pygeoip) [![Downloads](https://pypip.in/d/pygeoip/badge.png)](https://crate.io/packages/pygeoip)

## Installation

You can easily install pygeoip from PyPi.

```bash
pip install pygeoip
```

## Issues and Contribution

Bug reports are done by [creating an issue on Github](https://github.com/appliedsec/pygeoip/issues). If you want to contribute you can always [create a pull request](https://github.com/appliedsec/pygeoip/pulls) for discussion and code submission.

## Getting Started

Create your GeoIP instance with appropriate access flag. `STANDARD` reads data from disk when needed, `MEMORY_CACHE` loads database into memory on instantiation and `MMAP_CACHE` loads database into memory using mmap.

```python
>>> import pygeoip
>>> gi = pygeoip.GeoIP('/path/to/GeoIP.dat')
>>> gi.country_name_by_addr('64.233.161.99')
'United States'
```

### Country Lookup

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIP.dat')
>>> gi.country_code_by_name('google.com')
'US'
>>> gi.country_code_by_addr('64.233.161.99')
'US'
>>> gi.country_name_by_addr('64.233.161.99')
'United States'
```

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPv6.dat')
>>> gi.country_code_by_name('google.com')
'IE'
>>> gi.country_code_by_addr('2001:7fd::1')
'EU'
>>> gi.country_name_by_addr('2001:7fd::1')
'Europe'
```

### Region Lookup

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPRegion.dat')
>>> gi.region_by_name('apple.com')
{'region_code': 'CA', 'country_code': 'US'}
```

### City Lookup ###

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPCity.dat')
>>> gi.record_by_addr('64.233.161.99')
{
    'city': u'Mountain View',
    'region_code': u'CA',
    'area_code': 650,
    'time_zone': 'America/Los_Angeles',
    'dma_code': 807,
    'metro_code': 'San Francisco, CA',
    'country_code3': 'USA',
    'latitude': 37.41919999999999,
    'postal_code': u'94043',
    'longitude': -122.0574,
    'country_code': 'US',
    'country_name': 'United States',
    'continent': 'NA'
}
>>> gi.time_zone_by_addr('64.233.161.99')
'America/Los_Angeles'
```

### Organization Lookup

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPOrg.dat')
>>> gi.org_by_name('dell.com')
'Dell Computer Corporation'
```

### ISP Lookup

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPISP.dat')
>>> gi.isp_by_name('cnn.com')
'Turner Broadcasting System'
```

### ASN Lookup

```python
>>> gi = pygeoip.GeoIP('/path/to/GeoIPASNum.dat')
>>> gi.asn_by_name('cnn.com')
'AS5662 Turner Broadcasting'
```

For more information, [check out the full API documentation](http://packages.python.org/pygeoip).

## Supported Databases

| Type           | IPv4 | IPv6 | Details       |
| -------------- |:----:|:----:| -------------- | 
| Country        | ✓ | ✓ | [MaxMind Country product page](http://www.maxmind.com/en/country) |
| City           | ✓ | ✓ | [MaxMind City product page](http://www.maxmind.com/en/city) |
| Organization   | ✓ | | [MaxMind Organization product page](http://www.maxmind.com/en/organization) |
| ISP            | ✓ | | [MaxMind ISP product page](http://www.maxmind.com/en/isp) |
| Region         | ✓ | | [MaxMind Region product page](http://www.maxmind.com/en/geolocation_landing) |
| ASN            | ✓ | ✓ | [MaxMind ASN product page](http://dev.maxmind.com/geoip/legacy/geolite) |
| Netspeed       | ✓ | | [MaxMind Netspeed product page](http://www.maxmind.com/en/netspeed) |
