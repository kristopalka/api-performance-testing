#!/bin/bash

path="./results"

results_file="${path}/processed.json"
echo "{" > $results_file


file="./results/fastapi/hello/raw_1000rps_1.json"





find $path -type f -name 'raw_*rps_*.json' | while read -r file; do
    echo "Reviewing file ${file}"
    failed_line=$(grep -nE '^{"metric":"failed_counter","type":"Point","data":{"time":".*","value":1' "$file" | head -n 1 | cut -d: -f1)
    dropped_line=$(grep -nE '^{"metric":"dropped_iterations","type":"Point","data":{"time":".*","value":1' "$file" | head -n 1 | cut -d: -f1)


    if [ -z "$failed_line" ] && [ -z "$dropped_line" ]; then
        line=$(tail -n 1 "$file")
        line_number=$(grep -c "" "$file")
    else
        if [ -n "$failed_line" ] && [ -n "$dropped_line" ]; then
            if [ "$failed_line" -lt "$dropped_line" ]; then
                line=$(sed -n "${failed_line}p" "$file")
                line_number=${failed_line}
            else
                line=$(sed -n "$((dropped_line - 1))p" "$file")
                line_number=${dropped_line-1}
            fi
        elif [ -n "$failed_line" ]; then
            line=$(sed -n "${failed_line}p" "$file")
            line_number=${failed_line}
        elif [ -n "$dropped_line" ]; then
            line=$(sed -n "$((dropped_line - 1))p" "$file")
            line_number=${dropped_line-1}
        fi
    fi


    end=$(echo "$line" | grep -oP '"timestamp_start":"\K[^"]+')
    start=$(head -n 1 "$file" | grep -oP '"timestamp_start":"\K[^"]+')


    lines="\"${file}\": {\"start\": \"${start}\", \"end\": \"${end}\", \"processed_requests\": ${line_number}},"
    echo "${lines}" >> $results_file
done

result=$(< ${results_file})
result="${result::-1}}"
echo "$result" > $results_file