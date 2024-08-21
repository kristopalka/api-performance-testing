#!/bin/bash

filter_file() {
    local file="$1"
    local tempfile=$(mktemp)

    grep -E '(^{"metric":"http_req_stats","type":"Point")|(^{"metric":"dropped_iterations","type":"Point")' "$file" > "$tempfile"
    mv "$tempfile" "$file"
}

path="./../results/"

find $path -type f -name 'raw_*rps.json' | while read -r file; do
    echo "Cleaning file ${file}"
    filter_file "${file}"
done
