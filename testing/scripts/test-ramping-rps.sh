#!/bin/bash

source .topology_params

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --results-dir) RESULTS_DIR="$2"; shift 2 ;;
        -s|--service) SERVICE="$2"; shift 2 ;;
        -e|--endpoint) ENDPOINT="$2"; shift 2 ;;
        --warmup-rps) WARMUP_RPS="$2"; shift 2 ;;
        --warmup-duration) WARMUP_DURATION="$2"; shift 2 ;;
        --start-rps) START_RPS="$2"; shift 2 ;;
        --end-rps) END_RPS="$2"; shift 2 ;;
        -d|--duration) DURATION="$2"; shift 2 ;;
        --skip-warmup) SKIP_WARMUP=true; shift ;;
        --skip-restart) SKIP_RESTART=true; shift ;;
        *) echo "Unknown parameter passed: $1"; helpFunction ;;
    esac
done


RESULTS_DIR=${RESULTS_DIR:-"./../results/ramping_rps"}
SERVICE=${SERVICE:-"spring"}
ENDPOINT=${ENDPOINT:-"hello"}

WARMUP_RPS=${WARMUP_RPS:-32}
WARMUP_DURATION=${WARMUP_DURATION:-5}
WARMUP_ALLOCATED_VUS=50

START_RPS=${START_RPS:-1}
END_RPS=${END_RPS:-1024}
DURATION=${DURATION:-30}
ALLOCATED_VUS=20000


SKIP_WARMUP=${SKIP_WARMUP:-false}
SKIP_RESTART=${SKIP_RESTART:-false}

URL="${API_URL}/${ENDPOINT}"
OUTPUT_DIR="${RESULTS_DIR}/${SERVICE}/${ENDPOINT//\//_}"
mkdir -p "${OUTPUT_DIR}"


# ------------------------------- RESTART CONTAINER -------------------------------
if [ ${SKIP_RESTART} = false ]
then
  echo "Running service \"${SERVICE}\" on server..."
  sshpass -p "${SERVER_PASS}" ssh -l "${SERVER_USER}" "${SERVER_IP}" \
    "
    cd api-performance-testing/services/
    echo ' Stopping all containers...'
    docker stop \$(docker ps -a -q) >> /dev/null
    docker compose up -d mariadb ${SERVICE}
    "

  echo -n "Waiting for service to run"
  while [ "$(curl -sL -w '%{http_code}' "${API_URL}/database" -o /dev/null)" != "200" ]; do
      echo -n "."
      sleep 1
  done
  echo " Service started."
fi

# ------------------------------- LAZY INITIALIZATION WARMUP -------------------------------
if [ ${SKIP_WARMUP} = false ]
then
  echo "Warming up service..."
  k6 run \
    --env URL="${URL}" \
    --env RPS="${WARMUP_RPS}" \
    --env DURATION="${WARMUP_DURATION}" \
    --env ALLOCATED_VUS="${WARMUP_ALLOCATED_VUS}" \
    --no-summary --quiet \
    k6/const_rps.js
fi


# ------------------------------- TEST STAGE -------------------------------
STATS_FULL="count,avg,min,p(10),p(20),p(30),p(40),med,p(60),p(70),p(80),p(90),p(95),p(98),p(99),p(99.9),max"
STATS_NORMAL="count,avg,min,max"
RESULTS_FILE="${OUTPUT_DIR}/results_${DURATION}s_${START_RPS}_${END_RPS}rps.json"
RAW_FILE="${OUTPUT_DIR}/raw_${DURATION}s_${START_RPS}_${END_RPS}rps.json"

echo "Testing service..."
k6 run \
  --env URL="${URL}" \
  --env START_RPS="${START_RPS}" \
  --env END_RPS="${END_RPS}" \
  --env DURATION="${DURATION}" \
  --env ALLOCATED_VUS="${ALLOCATED_VUS}" \
  --summary-trend-stats="${STATS_NORMAL}" \
  --summary-export "${RESULTS_FILE}" \
  --out json="${RAW_FILE}" \
  --quiet \
  k6/ramping_rps.js

