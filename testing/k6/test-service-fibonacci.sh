#!/bin/bash

source .env
ENDPOINT="fibonacci"
DEFAULT_TESTED_SERVICE="fastapi"


helpFunction()
{
   echo ""
   echo "Usage: $0 [-s --tested-service]"
   echo -e "\t-s, --tested-service          Service base URL (default: $DEFAULT_TESTED_SERVICE)"
   exit 1
}

while [[ "$#" -gt 0 ]]; do
   case "$1" in
      -s|--tested-service) TESTED_SERVICE="$2"; shift ;;
      -h|--help) helpFunction; shift ;;
      *) echo "Unknown parameter passed: $1"; helpFunction ;;
   esac
   shift
done


TESTED_SERVICE=${TESTED_SERVICE:-$DEFAULT_TESTED_SERVICE}




echo "Running service \"${TESTED_SERVICE}\" on server..."
sshpass -p "${SERVER_PASS}" ssh -l "${SERVER_USER}" "${SERVER_IP}" \
  "
  cd api-performance-testing/services/
  echo ' Stopping all containers...'
  docker stop \$(docker ps -a -q) >> /dev/null
  docker compose up -d ${TESTED_SERVICE}
  "

echo -n "Waiting for service to run"
while [ "$(curl -sL -w '%{http_code}' "${SERVICE_URL}/${ENDPOINT}/10" -o /dev/null)" != "200" ]; do
    echo -n "."
    sleep 1
done
echo " Service started."


./endpoint.sh -u "${SERVICE_URL}" \
    --endpoint "${ENDPOINT}/10" \
    --output "./results/${TESTED_SERVICE}"

for N in 100 1000 10000
do
  ./endpoint.sh -u "${SERVICE_URL}" \
    --endpoint "${ENDPOINT}/${N}" \
    --output "${RESULTS_DIR}/${TESTED_SERVICE}" \
    --skip-warmup
done