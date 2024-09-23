import matplotlib.pyplot as plt
import pandas as pd

from vizualization.utils.const import *
from vizualization.utils.load import get_dataframe

executor = "const_rps/iter_0"

service = "fastapi"
endpoint = "hello"
metrics = ["sending", "waiting", "receiving", "duration", "connecting"]
duration = 120
rps_tab = list(range(10, 201, 10)) + list(range(250, 801, 50))
warmup_time = 20
show_errors = True


def calculate_params(key, df):
    measure_df = df[(df['time'] >= warmup_time) & (df['time'] < duration - 20) & (df['error'] == "0")]
    errors_number = df[df['error'] != "0"].shape[0]

    return {
        'key': key,
        'errors': errors_number,
        **{f'{metric}_mean': measure_df[metric].mean() for metric in metrics},
        **{f'{metric}_std': measure_df[metric].std() for metric in metrics}
    }


fig, ax_durations = plt.subplots(figsize=(10, 6))

dfs = {rps: get_dataframe(executor, service, endpoint, duration, rps) for rps in rps_tab}

results = []
for s, df in dfs.items():
    params = calculate_params(s, df)
    if params['errors'] == 0 or show_errors:
        results.append(params)

results_df = pd.DataFrame(results)



for metric in metrics:
    ax_durations.plot(results_df['key'], results_df[f'{metric}_mean'],
                      label=f'http_req_{metric}',
                      color=services_colors[service],
                      linestyle='--',
                      linewidth=1, marker=metrics_marker[metric],
                      markersize=8, alpha=metrics_alpha[metric], mec='black')

    # ax_durations.fill_between(results_df['key'],
    #                           results_df[f'{metric}_mean'] - results_df[f'{metric}_std'],
    #                           results_df[f'{metric}_mean'] + results_df[f'{metric}_std'],
    #                           color=metrics_color[metric], alpha=0.2)

ax_durations.set_xlabel('Obciążęnie RPS')
ax_durations.set_ylabel('Średni czas metryki [ms]')
plt.title(
    f'Średni czas oraz odchylenie standardowe metryk dla {service} \\{endpoint}, duration={duration}, warmup_time={warmup_time}')

ax_durations.set_yscale("log")
ax_durations.set_ylim(bottom=0)

if show_errors:
    ax_errors = ax_durations.twinx()
    ax_errors.plot(results_df['key'], results_df['errors'],
                   label=f'{service} suma błędów',
                   color="red",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5,
                   mfc='red', mec='black')

    lines, labels = ax_durations.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax_durations.legend(lines + lines2, labels + labels2, loc='upper left')

    ax_errors.set_ylim(bottom=0)
    ax_errors.set_ylabel('Liczba błędów')
else:
    ax_durations.legend()

plt.show()
