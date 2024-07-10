test="./test-ramping-rps.sh"
services=("spring" "flask" "fastapi" "gin")

start_time=$(date +%s.%N)

for service in "${services[@]}"; do
    for rps in 1; do
        echo "Testing ${service} with ${rps} rps"
        if [ $rps -eq 1 ]; then
            $test --service "$service"
        else
            $test --service "$service" --skip-warmup
        fi
        sleep 10
    done
done


end_time=$(date +%s.%N)
time=$(echo "$end_time - $start_time" | bc)
echo "Time spent on collecting data: ${time}"