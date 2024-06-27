TESTED_SERVICE="spring"

./test-service-hello.sh --tested-service ${TESTED_SERVICE}
./test-service-fibonacci.sh --tested-service ${TESTED_SERVICE}
./test-service-database.sh --tested-service ${TESTED_SERVICE}