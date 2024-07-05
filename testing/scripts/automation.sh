./test-endpoint.sh --vus 128 --service spring
./test-endpoint.sh --vus 256 --service spring --skip-warmup
./test-endpoint.sh --vus 512 --service spring --skip-warmup
./test-endpoint.sh --vus 1024 --service spring --skip-warmup
./test-endpoint.sh --vus 2048 --service spring --skip-warmup
./test-endpoint.sh --vus 4096 --service spring --skip-warmup
./test-endpoint.sh --vus 8192 --service spring --skip-warmup
./test-endpoint.sh --vus 16384 --service spring --skip-warmup
./test-endpoint.sh --vus 32768 --service spring --skip-warmup

./test-endpoint.sh --vus 128 --service flask
./test-endpoint.sh --vus 256 --service flask --skip-warmup
./test-endpoint.sh --vus 512 --service flask --skip-warmup
./test-endpoint.sh --vus 1024 --service flask --skip-warmup
./test-endpoint.sh --vus 2048 --service flask --skip-warmup
./test-endpoint.sh --vus 4096 --service flask --skip-warmup
./test-endpoint.sh --vus 8192 --service flask --skip-warmup
./test-endpoint.sh --vus 16384 --service flask --skip-warmup
./test-endpoint.sh --vus 32768 --service flask --skip-warmup

./test-endpoint.sh --vus 128 --service fastapi
./test-endpoint.sh --vus 256 --service fastapi --skip-warmup
./test-endpoint.sh --vus 512 --service fastapi --skip-warmup
./test-endpoint.sh --vus 1024 --service fastapi --skip-warmup
./test-endpoint.sh --vus 2048 --service fastapi --skip-warmup
./test-endpoint.sh --vus 4096 --service fastapi --skip-warmup
./test-endpoint.sh --vus 8192 --service fastapi --skip-warmup
./test-endpoint.sh --vus 16384 --service fastapi --skip-warmup
./test-endpoint.sh --vus 32768 --service fastapi --skip-warmup

./test-endpoint.sh --vus 128 --service gin
./test-endpoint.sh --vus 256 --service gin --skip-warmup
./test-endpoint.sh --vus 512 --service gin --skip-warmup
./test-endpoint.sh --vus 1024 --service gin --skip-warmup
./test-endpoint.sh --vus 2048 --service gin --skip-warmup
./test-endpoint.sh --vus 4096 --service gin --skip-warmup
./test-endpoint.sh --vus 8192 --service gin --skip-warmup
./test-endpoint.sh --vus 16384 --service gin --skip-warmup
./test-endpoint.sh --vus 32768 --service gin --skip-warmup