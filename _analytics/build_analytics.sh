#!/bin/bash

BASEDIR=$(dirname "$0")

if ! python3 -c 'import pyminifier' > /dev/null 2>&1 ; then
    echo Install pyminifier to use this script. > 2
    exit 1
fi

pyminifier "$BASEDIR/analytics_core.py" | grep -v '^#\|^\s*$' | \
           "$BASEDIR/analytics_pack.py" | fold -w 120
