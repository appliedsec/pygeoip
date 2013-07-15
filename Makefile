PANDOC := $(shell which pandoc)
VIRTUALENV := $(shell which virtualenv)

ifeq ($(PANDOC),)
$(warning No pandoc binary found)
endif

ifeq ($(VIRTUALENV),)
	$(warning No virtualenv binary found)
endif

all: deps test doc

venv:
	@virtualenv venv
	@venv/bin/pip install tox nose epydoc

test: venv
	@venv/bin/tox

doc: venv
	@venv/bin/epydoc --config=epydoc.ini --no-private
	@pandoc --from=markdown --to=rst --output=README.rst README.md
