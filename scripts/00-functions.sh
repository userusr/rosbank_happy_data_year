#!/bin/bash

cd "$(dirname "$0")"

get_overpass() {
    local url="https://overpass.kumi.systems/api/interpreter"
    local file=$1
    local query=$2

    echo "$query" | sed -e 's/^[[:space:]]*//'

    if [ ! -f "$file" ]; then
        curl --globoff -o $file $url --data-urlencode "data=${query//[$'\t\r\n']}"
    fi;
    echo "----------------------------------------------------"
}
