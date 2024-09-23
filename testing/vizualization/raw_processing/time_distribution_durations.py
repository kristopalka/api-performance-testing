import pandas as pd
from matplotlib import pyplot as plt

from vizualization.utils.const import services_colors, charts_dir
from vizualization.utils.load import get_dataframe

executor = "const_rps/iter_0"
service = "gin"
endpoint = "hello"
duration = 120
rps = 650

df = get_dataframe(executor, service, endpoint, duration, rps, force_process=True)

zoom = 1
left_margin = 40
right_margin = 60

if zoom == 1:
    df['time'] = df['time'].astype(int)
else:
    df['time'] = df['time'] * zoom
    df['time'] = df['time'].astype(int)
    df['time'] = df['time'] / zoom
    df = df[(df['time'] > left_margin) & (df['time'] < right_margin)]


result = df.groupby('time').apply(
    lambda x: pd.Series({
        'mean': x.loc[x['error'] == "0", 'duration'].mean(),
        'std': x.loc[x['error'] == "0", 'duration'].std(),
        'error_count': (x.loc[x['error'] != "0"].shape[0] / x.shape[0]) * 100
    })
).reset_index()


fig, ax_durations = plt.subplots(figsize=(10, 6))

ax_durations.plot(result['time'], result['mean'],
        label="Średni czad odpowiedzi", color=services_colors[service],
        linestyle='-', linewidth=1.5, marker="o")

ax_durations.fill_between(result['time'],
                          result['mean'] - result['std'],
                          result['mean'] + result['std'],
                          color=services_colors[service], alpha=0.2)

ax_durations.set_title(f'metric=http_req_duration, service={service}, endpoint={endpoint}, {executor}=({rps}), duration={duration}, sampling={1/zoom}s')
ax_durations.set_xlabel('Czas od rozpoczęcia eksperymentu [s]')
ax_durations.set_ylabel(f'Długość odpowiedzi [ms]')
ax_durations.grid(True)
ax_durations.set_ylim(bottom=0)
if zoom == 1:
    ax_durations.set_xlim(left=0, right=duration)

if df[df['error'] != "0"].shape[0] > 0:
    ax_errors = ax_durations.twinx()
    ax_errors.set_ylabel('Odsetek błędów [%]')

    ax_errors.plot(result['time'], result['error_count'],
                   label="odsetek błędów", color="black",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5, mec='black')

    lines, labels = ax_durations.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax_durations.legend(lines + lines2, labels + labels2, loc='upper left')
    ax_errors.set_ylim(bottom=0, top=100)

plt.subplots_adjust(left=0.09, bottom=0.1,  right=0.92, top=0.91)
fig.savefig(f'{charts_dir}/time_distribution_durations_errors_{service}_{endpoint}_{duration}_{rps}_{zoom}.svg', format='svg')
plt.show()
