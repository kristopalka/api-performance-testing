import pandas as pd
from matplotlib import pyplot as plt

from vizualization.utils.const import services_colors, services_colors_light
from vizualization.utils.load import get_dataframe

executor = "const_rps"
service = "spring"
endpoint = "hello"
duration = 120
rps = 950

df = get_dataframe(executor, service, endpoint, duration, rps, force_process=False)

zoom = 1
left_margin = 20
right_margin = 40

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
        'error_count': x.loc[x['error'] != "0"].shape[0]
    })
).reset_index()


fig, ax_durations = plt.subplots(figsize=(14, 8))

ax_durations.plot(result['time'], result['mean'],
        label="Średni czad odpowiedzi na żądanie", color=services_colors[service],
        linestyle='-', linewidth=1.5, marker="o")

ax_durations.fill_between(result['time'],
                          result['mean'] - result['std'],
                          result['mean'] + result['std'],
                          color=services_colors[service], alpha=0.2)

ax_durations.set_title(f'Średni czas odpowiedzi w czasie dla {service} /{endpoint}: rps={rps}, duration={duration}')
ax_durations.set_xlabel('Czas od rozpoczęcia eksperymentu')
ax_durations.set_ylabel('Średni czas odpowiedzi w danej sekundzie [ms]')
ax_durations.grid(True)
ax_durations.set_ylim(bottom=0)

if df[df['error'] != "0"].shape[0] > 0:
    ax_errors = ax_durations.twinx()
    ax_errors.set_ylabel('Liczba błędów')

    ax_errors.plot(result['time'], result['error_count'],
                   label="Liczba błędów", color="black",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5, mec='black')

    lines, labels = ax_durations.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax_durations.legend(lines + lines2, labels + labels2)
    ax_errors.set_ylim(bottom=0)

plt.show()