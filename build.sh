#!/bin/bash

function error {
    echo "Error: $1" 1>&2
    exit 1
}

if [ -z $(which pandoc) ]; then
    error "Missing pandoc binary"
fi

if [ -z $(which virtualenv) ]; then
    error "Missing virtualenv binary"
fi

if [ ! -d venv ]; then
	virtualenv venv || error "virtualenv failed"
	venv/bin/pip install tox nose epydoc || error "pip failed"
fi

venv/bin/tox || error "tox failed"
venv/bin/epydoc --config=epydoc.ini --no-private || error "epydoc failed"

pandoc -f markdown -t rst -o README.rst README.md || error "pandoc failed"

