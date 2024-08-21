import matplotlib.pyplot as plt
import pandas as pd

from vizualization.utils.const import services_colors, services_colors_light
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_confidence

executor = "const_rps"

services = ["flask", "fastapi", "spring", "gin"]  # "flask", "fastapi", "spring", "gin",
endpoint = "hello"
duration = 120
rps_tab = list(range(10, 201, 10)) + list(range(250, 1001, 50))
warmup_time = 20

metric = "duration"
show_errors = True
batch_size = duration - warmup_time


def calculate_params(key, df):
    measure_df = df[(df['time'] >= warmup_time) & (df['error'] == "0")]
    errors_number = df[df['error'] != "0"].shape[0]

    # measure_df['duration'] = measure_df['duration'] + measure_df['connecting']

    # measure_df.loc[:, 'time'] = (measure_df['time'] // batch_size).astype(int)
    # means = measure_df.groupby('time')[metric].mean().reset_index()

    mean = measure_df[metric].mean()
    std = measure_df[metric].std()
    conf = get_confidence(measure_df.shape[0], mean, std)

    return {
        'key': key,
        'mean': mean,
        'std': std,
        'conf': conf,
        'error_rate': errors_number / (measure_df.shape[0] + errors_number) * 100
    }


fig, ax = plt.subplots(figsize=(14, 8))
if show_errors:
    ax_errors = ax.twinx()

for service in services:
    dfs = {rps: get_dataframe(executor, service, endpoint, duration, rps) for rps in rps_tab}

    results = []
    for s, df in dfs.items():
        params = calculate_params(s, df)
        if params['error_rate'] == 0 or show_errors:
            results.append(params)

    results_df = pd.DataFrame(results)

    ax.plot(results_df['key'], results_df['mean'], label=f'{service} średni czas odpowiedzi',
            color=services_colors[service], linestyle='--', linewidth=1,
            marker='o', markersize=5)
    ax.fill_between(results_df['key'], results_df['mean'] - results_df['std'],
                    results_df['mean'] + results_df['std'],
                    color=services_colors[service], alpha=0.2)
    if show_errors:
        ax_errors.plot(results_df['key'], results_df['error_rate'],
                       label=f'{service} odsetek błędów',
                       color=services_colors_light[service],
                       linestyle='--', linewidth=1,
                       marker='x', markersize=5,
                       mfc='red', mec='black')

ax.set_xlabel('Obciążęnie RPS')
ax.set_ylabel('Średni czas odpowiedzi (ms)')
plt.title('Średni czas odpowiedzi na zapytanie oraz odchylenie standardowe\n'
          f'endpoint={endpoint}, duration={duration}, metric=http_req_{metric}, warmup_time={warmup_time}')

ax.set_yscale("log")
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.grid(True)

if show_errors:
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    ax_errors.set_ylim(bottom=0)
    ax_errors.set_ylabel('Odsetek błędów')
else:
    ax.legend()

plt.show()
