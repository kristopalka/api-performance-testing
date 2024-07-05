#!/bin/bash

source .topology_params
RESULTS_DIR="./../results"

SERVICE="gin"
ENDPOINT="hello"

WARMUP_DURATION=10
WARMUP_VUS=128


URL="${API_URL}/${ENDPOINT}"
OUTPUT_DIR="${RESULTS_DIR}/${SERVICE}/${ENDPOINT//\//_}"
mkdir -p "${OUTPUT_DIR}"

# ------------------------------- RUN CONTAINER -------------------------------

echo "Running service \"${SERVICE}\" on server..."
sshpass -p "${SERVER_PASS}" ssh -l "${SERVER_USER}" "${SERVER_IP}" \
  "
  cd api-performance-testing/services/
  echo ' Stopping all containers...'
  docker stop \$(docker ps -a -q) >> /dev/null
  docker compose up -d mariadb ${SERVICE}
  "

echo -n "Waiting for service to run"
while [ "$(curl -sL -w '%{http_code}' "${SERVICE_URL}/${ENDPOINT}" -o /dev/null)" != "200" ]; do
    echo -n "."
    sleep 1
done
echo " Service started."


# ------------------------------- TEST WARMUP -------------------------------

echo "Testing warmup..."
k6 run \
  --vus "${WARMUP_VUS}" --duration "${WARMUP_DURATION}s" \
  --env URL="${URL}" \
  --out json="${OUTPUT_DIR}/warmup_raw_${WARMUP_DURATION}s_${WARMUP_VUS}vus.json" \
  k6/script.js
