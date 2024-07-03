import json

import matplotlib.pyplot as plt
import pandas as pd

framework = "spring"
file = "hello_15s_1024vus"
metrics = "http_req_duration"

file_path = f"./../results/{framework}/raw_{file}.json"

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

plt.figure(figsize=(10, 6))
plt.scatter(df['time'], df['duration'], s=10, c='blue')
plt.title(f'Czasy odpowiedzi {metrics} dla {framework} {file}')
plt.xlabel('Czas')
plt.ylabel('Opóźnienie (ms)')
plt.grid(True)
plt.show()
