#!/bin/bash

DEFAULT_URL_BASE="http://10.0.0.1:8080"
DEFAULT_ENDPOINT="hello"
DEFAULT_OUTPUT_DIR="out"
DEFAULT_SKIP_WARMUP=false

helpFunction()
{
   echo ""
   echo "Usage: $0 [-u --url] [-e --endpoint] [-o --output] [-s --skip-warmup]"
   echo -e "\t-u, --url          Service base URL (default: $DEFAULT_URL_BASE)"
   echo -e "\t-e, --endpoint     Endpoint that will be tested (default: $DEFAULT_ENDPOINT)"
   echo -e "\t-o, --output       Output file directory (default: $DEFAULT_OUTPUT_DIR)"
   echo -e "\t-s, --skip-warmup  Script will skip warm-up phase"
   exit 1
}

while [[ "$#" -gt 0 ]]; do
   case "$1" in
      -u|--url) URL_BASE="$2"; shift ;;
      -e|--endpoint) ENDPOINT="$2"; shift ;;
      -o|--output) OUTPUT_DIR="$2"; shift ;;
      -s|--skip-warmup) SKIP_WARMUP=true; shift ;;
      -h|--help) helpFunction; shift ;;
      *) echo "Unknown parameter passed: $1"; helpFunction ;;
   esac
   shift
done


URL_BASE=${URL_BASE:-$DEFAULT_URL_BASE}
ENDPOINT=${ENDPOINT:-$DEFAULT_ENDPOINT}
OUTPUT_DIR=${OUTPUT_DIR:-$DEFAULT_OUTPUT_DIR}
SKIP_WARMUP=${SKIP_WARMUP:-$DEFAULT_SKIP_WARMUP}

mkdir -p "${OUTPUT_DIR}"
URL=""${URL_BASE}/${ENDPOINT}


# ------------------------------- CHECK STAGE -------------------------------
echo -n "Checking endpoint... "
if [ "$(curl -sL -w '%{http_code}' "${URL}" -o /dev/null)" = "200" ]; then
    echo "Success ${URL}"
else
    echo "Can not obtain response from ${URL}"
    exit 1
fi

sleep 0.5

# ------------------------------- WARMUP STAGE -------------------------------
if [ $SKIP_WARMUP == false ]
then
  echo "Warming up service..."
  k6 run \
    --vus 256 --duration "15s"\
    --env URL="${URL}" \
    --no-summary \
    constant-vus-endpoint.js

  sleep 10
fi


# ------------------------------- TEST STAGE -------------------------------
echo "Testing service..."
k6 run \
  --vus 1024 --duration "15s"\
  --env URL="${URL}" \
  --summary-trend-stats="count,avg,min,p(10),p(20),p(30),p(40),med,p(60),p(70),p(80),p(90),max" \
  --summary-export "${OUTPUT_DIR}/${ENDPOINT//\//_}_results.json" \
  constant-vus-endpoint.js
