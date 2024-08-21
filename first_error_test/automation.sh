test="./test-cut-off.sh"
services=("flask")  # "spring" "flask" "fastapi" "gin"

for service in "${services[@]}"; do
    for rps in 100 200 300 400 500; do
        echo "Testing ${service} with ${rps} rps"
        for i in 1 2 3 4 5; do
            $test  --service "$service" --rps "$rps" -i "$i"
            sleep 10
        done
    done
done