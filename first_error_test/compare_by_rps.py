from datetime import datetime, timezone
import re

import numpy as np
import pandas as pd
import ujson
from matplotlib import pyplot as plt
from scipy.stats import t

from const import services_colors


def load_file_by_path(path):
    with open(path, 'r') as file:
        return ujson.load(file)


results_file = "./results/processed.json"

rps_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
services = ['gin', 'spring', 'flask', 'fastapi']
endpoint = "hello"
samples = 10



data = load_file_by_path(results_file)
plt.figure(figsize=(10, 6))
for service in services:
    print(f'Processing {service}...')
    results = []
    for rps in rps_values:
        pattern = re.compile(f'\\./results/{service}/{endpoint}/raw_{rps}rps_\\d+\\.json')

        durations = []
        for key in data.keys():
            if pattern.match(key):
                start_date = datetime.strptime(data[key]['start'], "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date = datetime.strptime(data[key]['end'], "%Y-%m-%dT%H:%M:%S.%fZ")

                processed_count = int(data[key]['processed_requests'])
                duration = (end_date - start_date).total_seconds()

                durations.append(processed_count)  # can be changed to processed_count

        samples = len(durations)
        df = samples - 1  # stopnie swobody (degrees of freedom)
        alpha = 0.05  # poziom istotności
        t_critical = t.ppf(1 - alpha / 2, df)  # wartość krytyczna t


        mean = np.mean(durations)
        std = np.std(durations)
        margin_of_error = t_critical * (std / np.sqrt(samples))
        confidence_interval = (mean - margin_of_error, mean + margin_of_error)
        conf = (confidence_interval[1] - confidence_interval[0]) / 2

        print(f'{rps}: {durations}')

        results.append({
            'key': rps,
            'mean': mean,
            'std': std,
            'conf': conf,
        })

    df = pd.DataFrame(results)

    plt.plot(df['key'], df['mean'], label=service, color=services_colors[service], linestyle='--', linewidth=1, marker='o', markersize=5)
    plt.fill_between(df['key'], df['mean'] - df['std'], df['mean'] + df['std'], color=services_colors[service], alpha=0.2)


plt.xlabel('Obciążenie RPS')
plt.ylabel('Liczba obsłużonych zapytań do pierwszego błędu')
plt.title(f'endpoint={endpoint}, samples={samples}')

plt.ylim(bottom=0)
plt.grid(True)
plt.legend(loc='upper left')

plt.subplots_adjust(left=0.1, bottom=0.1,  right=0.96, top=0.91)
plt.savefig(f'./charts/request_count_to_first_error.svg', format='svg')
plt.show()
