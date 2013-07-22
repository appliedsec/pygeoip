Pure Python GeoIP API
=====================

This library is based on `Maxmind's GeoIP C
API <https://github.com/maxmind/geoip-api-c>`__.

Tested with Python version 2.5, 2.6, 2.7, 3.2 and 3.3.

|Build Status|

Installation
------------

You can easily install pygeoip from PyPi.

::

    pip install pygeoip

Supported Databases
-------------------

::

    * COUNTRY_EDITION
    * COUNTRY_EDITION_V6
    * REGION_EDITION_REV0
    * REGION_EDITION_REV1
    * CITY_EDITION_REV0
    * CITY_EDITION_REV1
    * CITY_EDITION_REV1_V6
    * ORG_EDITION
    * ISP_EDITION
    * ASNUM_EDITION
    * ASNUM_EDITION_V6

Issues and Contribution
-----------------------

Bug reports are done by `creating an issue on
Github <https://github.com/appliedsec/pygeoip/issues>`__. If you want to
contribute you can always `create a pull
request <https://github.com/appliedsec/pygeoip/pulls>`__ for discussion
and code submission.

Quick Documentation
-------------------

Create your GeoIP instance with appropriate access flag. ``STANDARD``
reads data from disk when needed, ``MEMORY_CACHE`` loads database into
memory on instantiation and ``MMAP_CACHE`` loads database into memory
using mmap.

::

    import pygeoip
    gi4 = pygeoip.GeoIP('/path/to/GeoIP.dat', pygeoip.MEMORY_CACHE)
    gi6 = pygeoip.GeoIP('/path/to/GeoIPv6.dat', pygeoip.MEMORY_CACHE)

Country Lookup
~~~~~~~~~~~~~~

::

    >>> gi4.country_code_by_name('google.com')
    'US'
    >>> gi4.country_code_by_addr('64.233.161.99')
    'US'
    >>> gi4.country_name_by_addr('64.233.161.99')
    'United States'
    >>> gi6.country_code_by_name('google.com')
    'IE'
    >>> gi6.country_code_by_addr('2001:7fd::1')
    'EU'
    >>> gi6.country_name_by_addr('2001:7fd::1')
    'Europe'

Region Lookup
~~~~~~~~~~~~~

::

    >>> gi = pygeoip.GeoIP('/path/to/GeoIPRegion.dat')
    >>> gi.region_by_name('apple.com')
    {'region_name': 'CA', 'country_code': 'US'}

City Lookup
~~~~~~~~~~~

::

    >>> gi = pygeoip.GeoIP('/path/to/GeoIPCity.dat')
    >>> gi.record_by_addr('64.233.161.99')
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
        'country_name': 'United States',
        'continent': 'NA'
    }
    >>> gi.time_zone_by_addr('64.233.161.99')
    'America/Los_Angeles'

Organization Lookup
~~~~~~~~~~~~~~~~~~~

::

    >>> gi = pygeoip.GeoIP('/path/to/GeoIPOrg.dat')
    >>> gi.org_by_name('dell.com')
    'Dell Computer Corporation'

ISP Lookup
~~~~~~~~~~

::

    >>> gi = pygeoip.GeoIP('/path/to/GeoIPISP.dat')
    >>> gi.org_by_name('cnn.com')
    'Turner Broadcasting System'

ASN Lookup
~~~~~~~~~~

::

    >>> gi = pygeoip.GeoIP('/path/to/GeoIPASNum.dat')
    >>> gi.org_by_name('cnn.com')
    'AS5662 Turner Broadcasting'

For more information, `check out the full API
documentation <http://packages.python.org/pygeoip>`__.

.. |Build Status| image:: https://travis-ci.org/appliedsec/pygeoip.png
   :target: https://travis-ci.org/appliedsec/pygeoip
