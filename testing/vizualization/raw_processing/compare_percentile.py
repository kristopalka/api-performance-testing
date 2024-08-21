import matplotlib.pyplot as plt
import pandas as pd

from vizualization.utils.const import *
from vizualization.utils.load import get_dataframe

executor = "const_rps"

service = "gin"
endpoint = "hello"
percentiles = [0, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99, 0.999, 1]
metric = "duration"
duration = 120
rps_tab = list(range(10, 201, 10))
warmup_time = 20
show_errors = True


def calculate_params(key, df):
    measure_df = df[(df['time'] >= warmup_time) & (df['error'] == "0")]
    errors_number = df[df['error'] != "0"].shape[0]

    return {
        'key': key,
        'error_rate': errors_number / (measure_df.shape[0] + errors_number) * 100,
        **{f'{percentile}': measure_df[metric].quantile(percentile) for percentile in percentiles},
    }


fig, ax_durations = plt.subplots(figsize=(14, 8))

dfs = {rps: get_dataframe(executor, service, endpoint, duration, rps) for rps in rps_tab}

results = []
for s, df in dfs.items():
    params = calculate_params(s, df)
    if params['error_rate'] == 0 or show_errors:
        results.append(params)

results_df = pd.DataFrame(results)



for i in range(1, len(percentiles)):
    ax_durations.fill_between(results_df['key'],
                              results_df[f'{percentiles[i-1]}'],
                              results_df[f'{percentiles[i]}'],
                              label=f'P({percentiles[i-1]}) - P({percentiles[i]})',
                              color=services_colors[service], alpha=1.0 - (i / (len(percentiles))))

for percentile in percentiles:
    ax_durations.plot(results_df['key'], results_df[f'{percentile}'],
                      color="black",
                      linestyle='-',
                      linewidth=0.6, marker="o",
                      markersize=1.5, alpha=0.4)

    if percentile == 0.5:
        ax_durations.plot(results_df['key'], results_df[f'{percentile}'],
                          label=f'P(0.5)',
                          color="black", linestyle='-', linewidth=1.2,
                          marker="o", markersize=1.6)

ax_durations.set_xlabel('Obciążęnie RPS')
ax_durations.set_ylabel('Średni czas odpowiedzi (ms)')
plt.title(
    f'Percentyle metryki http_req_{metric} dla {service} \\{endpoint}, duration={duration}, warmup_time={warmup_time}')

ax_durations.set_yscale("log")
ax_durations.set_ylim(bottom=0)
ax_durations.grid(True)

if show_errors:
    ax_errors = ax_durations.twinx()
    ax_errors.plot(results_df['key'], results_df['error_rate'],
                   label=f'odsetek błędów',
                   color="red",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5,
                   mfc='red', mec='black')

    lines, labels = ax_durations.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax_durations.legend(lines + lines2, labels + labels2, loc='upper left')

    ax_errors.set_ylim(bottom=0)
    ax_errors.set_ylabel('Odsetek błędów')
else:
    ax_durations.legend()

plt.show()
