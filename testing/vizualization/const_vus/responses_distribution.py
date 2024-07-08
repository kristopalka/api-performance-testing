import json

import matplotlib.pyplot as plt
import pandas as pd

framework = "fastapi"
endpoint = "hello"
duration = 10
vus = 128
file = f"warmup_raw_{duration}s_{vus}vus"
metrics = "http_req_duration"

file_path = f"./../results/const_vus/{framework}/{endpoint}/{file}.json"

with open(file_path, 'r') as f:
    raw_data = f.readlines()

json_data = [json.loads(line) for line in raw_data]

duration_data = [
    {
        'time': entry['data']['time'],
        'duration': entry['data']['value']
    }
    for entry in json_data if entry['type'] == 'Point' and entry['metric'] == metrics
]

df = pd.DataFrame(duration_data)
df['time'] = pd.to_datetime(df['time'])

df = df.sort_values(by='time')

# calculate date to time from starting experiment
start_time = df['time'].iloc[0]
df['time_elapsed'] = (df['time'] - start_time).dt.total_seconds()

# show chart
plt.figure(figsize=(10, 6))
plt.scatter(df['time_elapsed'], df['duration'], s=10, c='blue')
plt.title(f'Wartości metryki {metrics} w czasie warmup dla frameworku {framework}\nendpoint={endpoint}, vus={vus}, duration={duration}')
plt.xlabel('Czas od rozpoczęcia eksperymentu (sekundy)')
plt.ylabel('Czas odpowiedzi na pojedyncze zapytanie (ms)')
plt.grid(True)
plt.show()
