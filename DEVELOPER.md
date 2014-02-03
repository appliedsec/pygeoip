# Bootstrap manual for developers
_Dependencies: tox, nose_

### Testing

For testing we are using tox virtualenv-based Python version testing
and nose as test framwork.

Tox will create virtualenvs for all Python version pygeoip supports
and installs the current working tree using the setup.py install script.
Running the tests requires a couple of sample databases found on the
link below.

Maxmind sample databases for testing can be downloaded here:
https://www.defunct.cc/maxmind-geoip-samples.tar.gz (17 MB)

Extract the tarball in the tests directory and run `tox` from the root directory.

This requires a machine with Python 2.6 - 3.3 installed and all dependencies mention in the header.

### TL;DR

There's a Makefile doing all this for you.

    make test
