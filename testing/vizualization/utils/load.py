import os

import pandas as pd
import ujson

path_base = "./../../results"


def load_results(file):
    with open(file, 'r') as file:
        return ujson.load(file)


def load_raw_by_metric(path, *metrics):
    with open(path, 'r') as file:
        for line in file:
            json_object = ujson.loads(line)
            if json_object['type'] == "Point" and json_object['metric'] in metrics:
                yield json_object


def load_durations_dataframe(raw_file_path):
    json_generator = load_raw_by_metric(raw_file_path, 'http_req_duration', 'dropped_iterations')

    data = [
        {
            'time': entry['data']['time'],
            'duration': entry['data'].get('value', 0),
            'error': 0 if entry['metric'] == 'http_req_duration' and entry['data']['tags'][
                'expected_response'] == "true" else
            1 if entry['metric'] == 'dropped_iterations' else
            int(entry['data']['tags']['error_code'])
        }
        for entry in json_generator
    ]

    df = pd.DataFrame(data)
    start_time = pd.to_datetime(df['time'].iloc[0])

    df.loc[df['error'] == 1211, 'duration'] = 30000  # jeżeli error == i/o timeout to duration ustaw na 30 sekund
    df['time'] = (pd.to_datetime(df['time'])  # zamień string time na datetime
                  .sub(start_time).dt.total_seconds()  # ox to czas od startu a nie godzina
                  .sub(df['duration'] / 1000))  # ox to moment wysłania zapytania a nie otrzymania odpowiedzi

    return df


def get_dataframe(executor, service, endpoint, duration, rps):
    path = f"{path_base}/{executor}/{service}/{endpoint}"
    file_raw = f'{path}/raw_{duration}s_{rps}rps.json'
    file_proc = f'{path}/proc_{duration}s_{rps}rps.csv'

    if os.path.isfile(file_proc):
        print(f'Reading data from {file_proc}')
        return pd.read_csv(file_proc)
    else:
        print(f'Processing data from {file_raw}')
        df = load_durations_dataframe(file_raw)
        df.to_csv(file_proc)
        return df
