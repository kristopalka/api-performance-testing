import pandas as pd
from matplotlib import pyplot as plt

from vizualization.utils.load import load_json_by_metric

service = "fastapi"
endpoint = "hello"
duration = 10
rps = 10000
file = f"raw_{duration}s_{rps}rps"

file_path = f"./../../results/const_rps/{service}/{endpoint}/{file}.json"

data = []

for record in load_json_by_metric(file_path, 'http_req_duration', 'dropped_iterations'):
    if record['metric'] == 'http_req_duration':
        data.append({
            'time': record['data']['time'],
            'duration': record['data']['value'],
            'error': 0 if record['data']['tags']['expected_response'] == "true" else int(record['data']['tags']['error_code'])
        })
    elif record['metric'] == 'dropped_iterations':
        data.append({
            'time': record['data']['time'],
            'duration': 0,
            'error': 1
        })


df = pd.DataFrame(data)
start_time = pd.to_datetime(df['time'][0])

df.loc[df['error'] == 1211, 'duration'] = 30000     # jeżeli error == i/o timeout to duration ustaw na 30 sekund
df['time'] = (pd.to_datetime(df['time'])            # zamień string time na datetime
              .sub(start_time).dt.total_seconds()   # ox to czas od startu a nie godzina
              .sub(df['duration'] / 1000))          # ox to moment wysłania zapytania a nie otrzymania odpowiedzi

error_dict = {
    0: {'desc': 'HTTP 200', 'color': 'blue', 'count': (df['error'] == 0).sum()},
    1: {'desc': 'Dropped iterations', 'color': 'green', 'count': (df['error'] == 1).sum()},
    1211: {'desc': 'Dial: i/o timeout', 'color': 'orange', 'count': (df['error'] == 1211).sum()},
    1050: {'desc': 'Request timeout', 'color': 'purple', 'count': (df['error'] == 1050).sum()},
    1220: {'desc': 'Read: reset by peer', 'color': 'red', 'count': (df['error'] == 1220).sum()}
}

print(f"Should be sent: {duration * rps}")
print(f"Was sent: {df.shape[0]}")
for key in error_dict.keys():
    print(f"{error_dict[key]['desc']}: {error_dict[key]['count']}")

fig, ax = plt.subplots(figsize=(14, 8))

groups = df.groupby('error')
for error, group in groups:
    plt.scatter(group['time'], group['duration'],
                s=5,
                color=error_dict[error]['color'],
                label=f"{error_dict[error]['desc']}: {error_dict[error]['count']}")

ax.set_title(f'Rozkład odpowiedzi serwisu {service}: endpoint={endpoint}, rps={rps}, duration={duration}')
ax.set_xlabel('Czas w którym wysłano odpowiedź (sekundy)')
ax.set_ylabel('Ile czasu czekano na otrzymanie odpowiedzi lub stwierdzenie błędu (ms)')
ax.grid(True)
plt.xlim(left=0)
plt.legend()
fig.savefig(f'out/responses_distribution_{service}_{file}.png', format='png')
plt.show()
