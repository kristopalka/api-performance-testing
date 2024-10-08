#!/bin/bash

source .topology_params

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -r|--results-dir) RESULTS_DIR="$2"; shift 2 ;;
        -s|--service) SERVICE="$2"; shift 2 ;;
        -e|--endpoint) ENDPOINT="$2"; shift 2 ;;
        --warmup-vus) WARMUP_VUS="$2"; shift 2 ;;
        --warmup-duration) WARMUP_DURATION="$2"; shift 2 ;;
        -v|--vus) VUS="$2"; shift 2 ;;
        -d|--duration) DURATION="$2"; shift 2 ;;
        --skip-warmup) SKIP_WARMUP=true; shift ;;
        --skip-restart) SKIP_RESTART=true; shift ;;
        *) echo "Unknown parameter passed: $1"; helpFunction ;;
    esac
done

RESULTS_DIR=${RESULTS_DIR:-"./../results/const_vus"}
SERVICE=${SERVICE:-"flask"}
ENDPOINT=${ENDPOINT:-"hello"}

WARMUP_VUS=${WARMUP_VUS:-128}
WARMUP_DURATION=${WARMUP_DURATION:-10}

VUS=${VUS:-4096}
DURATION=${DURATION:-150}


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
  while [ "$(curl -sL -w '%{http_code}' "${URL}" -o /dev/null)" != "200" ]; do
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
    --vus "${WARMUP_VUS}" --duration "${WARMUP_DURATION}s" \
    --env URL="${URL}" \
    --no-summary \
    k6/const_vus.js
fi


# ------------------------------- TEST STAGE -------------------------------
echo "Testing service..."
k6 run \
  --vus "${VUS}" --duration "${DURATION}s" \
  --env URL="${URL}" \
  --summary-trend-stats="count,avg,min,p(10),p(20),p(30),p(40),med,p(60),p(70),p(80),p(90),p(95),p(98),p(99),p(99.9),max" \
  --summary-export "${OUTPUT_DIR}/results_${DURATION}s_${VUS}vus.json" \
  --out json="${OUTPUT_DIR}/raw_${DURATION}s_${VUS}vus.json" \
  k6/const_vus.js

