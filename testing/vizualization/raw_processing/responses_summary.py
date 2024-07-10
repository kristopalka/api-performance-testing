from vizualization.utils.utils import get_error_codes_counts

from vizualization.utils.const import error_codes
from vizualization.utils.load import load_results, get_dataframe

executor = "ramping_rps"
service = "gin"
endpoint = "hello"
duration = 150
start_rps = 32
end_rps = 16384

df = get_dataframe(executor, service, endpoint, duration, f'{start_rps}_{end_rps}')
results = load_results(executor, service, endpoint, duration, f'{start_rps}_{end_rps}')

errors_counts = get_error_codes_counts(df)

print(f"Should be sent: {duration * (start_rps + end_rps) / 2}")
print("------------- RAW SOURCE -------------")
print(f"Was sent: {df.shape[0]}")
for key in error_codes.keys():
    print(f"{error_codes[key]['desc']}: {error_codes[key]['count']}")

print("------------- RAW SOURCE -------------")
print(f"Tried to sent: {results['metrics']['http_reqs']['count'] + results['metrics']['dropped_iterations']['count']}")
print(f"http_reqs.counts: {results['metrics']['http_reqs']['count']}")
print(f"http_reqs_expected_response.counts: {results['metrics']['http_req_duration{expected_response:true}']['count']}")
print(f"dropped_iterations.counts: {results['metrics']['dropped_iterations']['count']}")
