#!/bin/bash

BASEDIR=$(dirname "$0")

lead='^# Analytics core$'
tail='^# End analytics core$'

if ! which perl > /dev/null ; then
    echo "You must install perl for this script to function."
    exit 1
fi

if [ ! "$1" ] ; then
    echo "You must specify an substitute file or '-' for stdin."
    exit 1
elif [ x"$1" = x"-" ] ; then
    insert_file="$(mktemp)"
    rm_insert_file=yes
    cat > "$insert_file"
elif [ ! -f "$1" ] ; then
    echo "Substiute file $1 does not exist or is unreadable."
    exit 1
else
    insert_file="$1"
fi

for cogdir in ../*/ ; do
    cogname="$(basename "${cogdir}")"
    cogfile="../${cogname}/${cogname}.py"
    if [ -f "$cogfile" ]; then
        echo $cogname
        # https://superuser.com/a/440057
        output="$(sed -e "/$lead/,/$tail/{ /$lead/{p; r ${insert_file}
                          }; /$tail/p; d }" "$cogfile")"
        cp "$cogfile" "$cogfile".bak
        echo "$output" > "$cogfile"
    fi
done

[ $rm_insert_file ] && rm -f "$insert_file"
