#!/bin/sh

if ! python3 -c 'import pyminifier' > /dev/null 2>&1 ; then
    echo Install pyminifier to use this script. > 2
    exit 1
fi

pyminifier analytics_core.py | grep -v '^#\|^\s*$' | ./analytics_pack.py | fold -w 120
