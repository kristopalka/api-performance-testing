test="./test-const-rps.sh"
services=("spring" "flask" "fastapi" "gin")  # "spring" "flask" "fastapi" "gin"

for service in "${services[@]}"; do
    for rps in 850 900 950 1000; do
        echo "Testing ${service} with ${rps} rps"
        $test  --service "$service" --rps "$rps" --duration 120
        sleep 30
    done
done
