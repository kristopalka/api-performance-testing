import os
import re
import warnings

import pandas as pd
import ujson

path_base = "./../../results"
warnings.simplefilter(action='ignore', category=FutureWarning)

def load_results(executor, service, endpoint, duration, rps):
    path = f"{path_base}/{executor}/{service}/{endpoint}"
    file_path = f'{path}/results_{duration}s_{rps}rps.json'
    return load_results_by_path(file_path)


def load_results_by_path(path):
    with open(path, 'r') as file:
        return ujson.load(file)


def load_raw_by_metric(path, *metrics):
    pattern = "^" + "|".join(f'{{\"metric":"{metric}"' for metric in metrics)
    regex = re.compile(pattern)

    with open(path, 'r') as file:
        for line in file:
            if regex.search(line):
                yield ujson.loads(line)


def load_durations_dataframe(raw_file_path):
    json_generator = load_raw_by_metric(raw_file_path, 'http_req_stats', 'dropped_iterations')

    data = []
    for entry in json_generator:
        if entry['metric'] == 'http_req_stats':
            data.append({
                'time': entry['data']['tags']['timestamp_start'],
                'duration': float(entry['data']['tags']['duration']),
                'blocked': float(entry['data']['tags']['blocked']),
                'connecting': float(entry['data']['tags']['connecting']),
                'receiving': float(entry['data']['tags']['receiving']),
                'sending': float(entry['data']['tags']['sending']),
                'waiting': float(entry['data']['tags']['waiting']),
                'error': entry['data']['tags']['error']
            })
        elif entry['metric'] == 'dropped_iterations':
            data.append({
                'time': entry['data']['time'],
                'duration': 0.0,
                'error': 'drop'
            })

    df = pd.DataFrame(data)
    df.sort_values(by='time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    start_time = pd.to_datetime(df['time'][0])- pd.Timedelta(seconds=0.2)
    df['time'] = (pd.to_datetime(df['time'], utc=True)  # zamień string time na datetime
                  .sub(start_time).dt.total_seconds())  # ox to czas od startu a nie godzina

    return df


def get_dataframe(executor, service, endpoint, duration, rps, force_process=False, path_to_results=path_base):
    path = f"{path_to_results}/{executor}/{service}/{endpoint}"
    file_raw = f'{path}/raw_{duration}s_{rps}rps.json'
    file_proc = f'{path}/proc_{duration}s_{rps}rps.csv'

    if os.path.isfile(file_proc) and not force_process:
        # print(f'Reading data from {file_proc}')
        dtype_dict = {
            'time': 'float64',
            'duration': 'float64',
            'error': 'string'
        }
        return pd.read_csv(file_proc, dtype=dtype_dict, index_col=0)
    else:
        # print(f'Processing data from {file_raw}')
        df = load_durations_dataframe(file_raw)
        df.to_csv(file_proc)
        return df


def save_df(df, filename):
    path = f"{path_base}/{filename}"
    df.to_csv(path)

def read_df(filename):
    path = f"{path_base}/{filename}"
    return pd.read_csv(path)