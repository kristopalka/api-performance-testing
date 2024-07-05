import json

from vizualization.utils.load import load_raw, load_results
from vizualization.utils.utils import *

path_base = "./../results"

service = "flask"
endpoint = "hello"
duration = 150
vus = '4096'
metrics = "http_req_duration"

file_raw = f'{path_base}/{service}/{endpoint}/raw_{duration}s_{vus}vus.json'
file_results = f'{path_base}/{service}/{endpoint}/results_{duration}s_{vus}vus.json'


raw_data = load_raw(file_raw)
results_data = load_results(file_results)

requests_number = 0
for entry in raw_data:
    if entry['type'] == 'Point' and entry['metric'] == 'http_reqs':
        requests_number += 1

print(requests_number)

# duration_data = [
#     {
#         'time': entry['data']['time'],
#         'duration': entry['data']['value']
#     }
#     for entry in raw_data if entry['type'] == 'Point' and entry['metric'] == 'http_reqs'
# ]

# df = pd.DataFrame(duration_data)
# df['time'] = pd.to_datetime(df['time'])
#
# df = df.sort_values(by='time')
#
# plt.figure(figsize=(10, 6))
# plt.scatter(df['time'], df['duration'], s=10, c='blue')
# plt.title(f'Czasy odpowiedzi {metrics} dla {framework} {file}')
# plt.xlabel('Czas')
# plt.ylabel('Opóźnienie (ms)')
# plt.grid(True)
# plt.show()
