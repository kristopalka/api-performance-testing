import matplotlib.pyplot as plt
import pandas as pd

from vizualization.utils.const import services_colors, charts_dir
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_confidence

executor = "const_rps"

services = ["flask", "fastapi", "spring", "gin"]  # "flask", "fastapi", "spring", "gin",
services = ["flask", "fastapi", "flask_5w", "fastapi_5w"]  # "flask", "fastapi", "spring", "gin",

endpoint = "hello"
duration = 120
rps_tab = list(range(10, 201, 10)) + list(range(250, 1001, 50)) #+ list(range(1100, 1401, 100))
warmup_time = 20

metric = "duration"
show_errors = False
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
        'error_rate': errors_number / (measure_df.shape[0] + errors_number) * 100 if errors_number != 0 else None
    }


fig, ax = plt.subplots(figsize=(10, 6))
if show_errors:
    ax_errors = ax.twinx()

for service in services:
    dfs = {rps: get_dataframe(executor, service, endpoint, duration, rps) for rps in rps_tab}


    results = []
    for s, df in dfs.items():
        params = calculate_params(s, df)
        if params['error_rate'] == None or show_errors:
            results.append(params)

    results_df = pd.DataFrame(results)


    if "5w" in service:
        ax.plot(results_df['key'], results_df['mean'], label=f'{service}',
                color=services_colors[service], linestyle='--', linewidth=1,
                marker='o', markersize=6,
                markeredgewidth=0.8, markeredgecolor='black')
        ax.fill_between(results_df['key'], results_df['mean'] - results_df['std'],
                        results_df['mean'] + results_df['std'],
                        color=services_colors[service], alpha=0.2)

    else:
        ax.plot(results_df['key'], results_df['mean'], label=f'{service}',
                color=services_colors[service], linestyle='--', linewidth=1,
                marker='o', markersize=5, alpha=0.5)
        ax.fill_between(results_df['key'], results_df['mean'] - results_df['std'],
                        results_df['mean'] + results_df['std'],
                        color=services_colors[service], alpha=0.1)


    if show_errors:
        ax_errors.plot(results_df['key'], results_df['error_rate'],
                       label=f'{service} błędy',
                       color=services_colors[service],
                       linestyle='--', linewidth=1,
                       marker='x', markersize=5, alpha=0.8,
                       mfc='red', mec='black')

ax.set_xlabel('Obciążęnie RPS')
ax.set_ylabel('Czas odpowiedzi [ms]')
plt.title(f'metric=http_req_{metric}, endpoint={endpoint}, duration={duration}, warmup_time={warmup_time}')

# ax.set_yscale("log")
ax.set_ylim(bottom=0.6, top=8)
ax.set_xlim(left=0, right=1010)
ax.grid(True)

if show_errors:
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    ax_errors.set_ylim(bottom=0, top=100)
    ax_errors.set_ylabel('Odsetek błędów [%]')
else:
    ax.legend(loc='upper left')

plt.subplots_adjust(left=0.07, bottom=0.1,  right=0.97, top=0.93)
fig.savefig(f'{charts_dir}/compare_average_services_{endpoint}_{duration}_5w.svg', format='svg')
plt.show()
