test="./test-endpoint-const-rps.sh"
services=("spring" "flask" "fastapi" "gin")

start_time=$(date +%s.%N)

for service in "${services[@]}"; do
    for rps in 512; do
        echo "Testing ${service} with ${rps} rps"
        if [ $rps -eq 512 ]; then
            $test --rps $rps --service "$service"
        else
            $test --rps $rps --service "$service" --skip-warmup
        fi
    done
done


end_time=$(date +%s.%N)
time=$(echo "$end_time - $start_time" | bc)
echo "Time spent on collecting data: ${time}"