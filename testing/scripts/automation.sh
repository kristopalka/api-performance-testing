test="./test-const-rps.sh"


#for i in 5; do
#    dir="./../results/const_rps/iter_${i}"
#    for service in "gin"; do
#        for rps in 400; do
#            echo "Testing ${service} with ${rps} rps -> ${dir}"
#            $test  --service "$service" --rps "$rps" --duration 120 --results-dir "$dir" --skip-warmup
#            sleep 5
#        done
#    done
#done



$test  --service "gin" --rps 110 --duration 120 --results-dir "./../results/const_rps/iter_2"
sleep 20
$test  --service "gin" --rps 450 --duration 120 --results-dir "./../results/const_rps/iter_3"
$test  --service "gin" --rps 500 --duration 120 --results-dir "./../results/const_rps/iter_5"
$test  --service "gin" --rps 550 --duration 120 --results-dir "./../results/const_rps/iter_1"