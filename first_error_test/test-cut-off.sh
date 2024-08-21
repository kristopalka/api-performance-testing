#!/bin/bash

filter_file() {
    local file="$1"
    local tempfile=$(mktemp)

    grep -E '(^{"metric":"failed_counter","type":"Point")|(^{"metric":"dropped_iterations","type":"Point")' "$file" > "$tempfile"
    mv "$tempfile" "$file"
}

source .topology_params

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --results-dir) RESULTS_DIR="$2"; shift 2 ;;
        -s|--service) SERVICE="$2"; shift 2 ;;
        -e|--endpoint) ENDPOINT="$2"; shift 2 ;;
        --warmup-rps) WARMUP_RPS="$2"; shift 2 ;;
        --warmup-duration) WARMUP_DURATION="$2"; shift 2 ;;
        -r|--rps) RPS="$2"; shift 2 ;;
        -d|--duration) DURATION="$2"; shift 2 ;;
        -i) I="$2"; shift 2 ;;
        --skip-warmup) SKIP_WARMUP="true"; shift ;;
        --skip-restart) SKIP_RESTART="true"; shift ;;
        *) echo "Unknown parameter passed: $1"; helpFunction ;;
    esac
done

RESULTS_DIR=${RESULTS_DIR:-"./results"}
SERVICE=${SERVICE:-"spring"}
ENDPOINT=${ENDPOINT:-"hello"}

WARMUP_RPS=${WARMUP_RPS:-32}
WARMUP_DURATION=${WARMUP_DURATION:-5}
WARMUP_ALLOCATED_VUS=50


I=${I:-0}
RPS=${RPS:-900}
DURATION=${DURATION:-120}
ALLOCATED_VUS=20000


SKIP_WARMUP=${SKIP_WARMUP:-"false"}
SKIP_RESTART=${SKIP_RESTART:-"false"}

URL="${API_URL}/${ENDPOINT}"
OUTPUT_DIR="${RESULTS_DIR}/${SERVICE}/${ENDPOINT//\//_}"
mkdir -p "${OUTPUT_DIR}"



# ------------------------------- RESTART CONTAINER -------------------------------
if [ "$SKIP_RESTART" == "false" ]; then
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


# ------------------------------- TEST STAGE -------------------------------
STATS_NORMAL="count,avg,min,max"


echo "Testing service..."
RESULTS_FILE="${OUTPUT_DIR}/results_${RPS}rps_${I}.json"
RAW_FILE="${OUTPUT_DIR}/raw_${RPS}rps_${I}.json"

k6 run \
  --env URL="${URL}" \
  --env RPS="${RPS}" \
  --env DURATION="${DURATION}" \
  --env ALLOCATED_VUS="${ALLOCATED_VUS}" \
  --summary-trend-stats="${STATS_NORMAL}" \
  --summary-export "${RESULTS_FILE}" \
  --out json="${RAW_FILE}" \
  cut_off.js

filter_file "${RAW_FILE}"


