# Pure Python GeoIP API #
The API is based on [MaxMind's C-based Python API](http://www.maxmind.com/app/python),
but the code itself is ported from the [Pure PHP GeoIP API](http://pear.php.net/package/Net_GeoIP) by Jim Winstead and Hans Lellelid.

It is mostly a drop-in replacement, except the `new` and `open` methods are gone.

Tested using tox with Python version 2.5, 2.6, 2.7, 3.0 and 3.1.

## Issues and contribution ##

Bug reports are done by [creating an issue on Github](https://github.com/appliedsec/pygeoip/issues). If you want to contribute you can always [create a pull request](https://github.com/appliedsec/pygeoip/pulls) for discussion and code submission.

## Installation ##

You can easily install pygeoip with setuptools:

    easy_install pygeoip

## Supported Databases ##

* Country
* Region
* City
* Organization
* ISP

## Quick Documentation ##

Create your GeoIP instance with appropriate access flag. `STANDARD` reads data from disk when needed, `MEMORY_CACHE` loads database into memory on instantiation and `MMAP_CACHE` loads database into memory using mmap.

    import pygeoip
    gi = pygeoip.GeoIP('/path/to/GeoIP.dat', pygeoip.MEMORY_CACHE)

### Country lookup ###

    >>> gi.country_code_by_name('google.com')
    'US'
    >>> gi.country_code_by_addr('64.233.161.99')
    'US'
    >>> gi.country_name_by_addr('64.233.161.99')
    'United States'

### City lookup ###

    >>> gic = pygeoip.GeoIP('/path/to/GeoIPCity.dat')
    >>> gic.record_by_addr('64.233.161.99')
    {
      'city': 'Mountain View',
    	'region_name': 'CA',
    	'area_code': 650,
    	'longitude': -122.0574,
    	'country_code3': 'USA',
    	'latitude': 37.419199999999989,
    	'postal_code': '94043',
    	'dma_code': 807,
    	'country_code': 'US',
    	'country_name': 'United States'
    }

### Timezone lookup ###

    >>> gic = pygeoip.GeoIP('/path/to/GeoIPCity.dat')
    >>> gic.time_zone_by_addr('64.233.161.99')
    'America/Los_Angeles'

For more information, [check out the full API documentation](http://packages.python.org/pygeoip).