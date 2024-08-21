import pandas as pd
from matplotlib import pyplot as plt

from vizualization.utils.const import services_colors, services_colors_light
from vizualization.utils.load import get_dataframe

executor = "const_rps"
service = "spring"
endpoint = "hello"
duration = 120
rpses = range(550, 1001, 50)
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']



fig, ax_durations = plt.subplots(figsize=(14, 8))
ax_errors = ax_durations.twinx()

i = 0
for rps in rpses:
    df = get_dataframe(executor, service, endpoint, duration, rps, force_process=False)
    df['time'] = df['time'].astype(int)

    result = df.groupby('time').apply(
        lambda x: pd.Series({
            'mean': x.loc[x['error'] == "0", 'duration'].mean(),
            'std': x.loc[x['error'] == "0", 'duration'].std(),
            'error_count': x.loc[x['error'] != "0"].shape[0]
        })
    ).reset_index()


    # ax_durations.plot(result['time'], result['mean'],
    #         label="Średni czad odpowiedzi na żądanie", color=services_colors[service],
    #         linestyle='-', linewidth=1.5, marker="o", alpha=0.5)
    #
    # ax_durations.fill_between(result['time'],
    #                           result['mean'] - result['std'],
    #                           result['mean'] + result['std'],
    #                           color=services_colors[service], alpha=0.2)

    ax_errors.plot(result['time'], result['error_count'],
                   label=f'Liczba błędów {rps} RPS', color="black",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5, mec=colors[i])
    i+= 1



ax_durations.set_title(f'Rozkład średniego czasu odpowiedzi w czasie dla wartości RPS {service} /{endpoint}')
ax_durations.set_xlabel('Czas od rozpoczęcia eksperymentu')
ax_durations.set_ylabel('Średni czas odpowiedzi w danej sekundzie [ms]')
ax_durations.grid(True)
ax_durations.set_ylim(bottom=0)


ax_errors.set_ylabel('Liczba błędów')

lines, labels = ax_durations.get_legend_handles_labels()
lines2, labels2 = ax_errors.get_legend_handles_labels()
ax_durations.legend(lines + lines2, labels + labels2)
ax_errors.set_ylim(bottom=0)

plt.show()
