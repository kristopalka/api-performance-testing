from matplotlib import pyplot as plt

from vizualization.utils.const import metrics_colors
from vizualization.utils.load import get_dataframe

executor = "const_rps"
metrics = ["sending", "waiting", "receiving", "duration", "connecting"]
service = "fastapi"
endpoint = "hello"
duration = 120
rps = 100

time_start = 0
time_stop = duration

df = get_dataframe(executor, service, endpoint, duration, rps)

df['time'] = df['time'].astype(int)

ok_df = df.loc[df['error'] == "0"]

fig, ax = plt.subplots(figsize=(14, 8))
for metric in metrics:
    mean = ok_df.groupby('time')[metric].mean().reset_index(name='mean')
    std = ok_df.groupby('time')[metric].mean().reset_index(name='std')

    ax.plot(mean['time'], mean['mean'],
            label=f'{metric}', color=metrics_colors[metric],
            linestyle='-', linewidth=1.5, marker="o")

    ax.fill_between(std['time'],
                    mean['mean'] - std['std'],
                    mean['mean'] + std['std'],
                    color=metrics_colors[metric], alpha=0.2)

ax.set_title(f'Średni czas odpowiedzi w każdej sekundzie dla {service} /{endpoint}: '
             f'rps={rps}, duration={duration}')
ax.set_xlabel('Czas od rozpoczęcia eksperymentu')
ax.set_ylabel('Średni czas odpowiedzi w danej sekundzie [ms]')

ax.grid(True)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.legend()

if df[df['error'] != "0"].shape[0] > 0:
    errors_counts = df.loc[df['error'] != "0"].groupby('time').size().reset_index(name='error_count')

    ax_errors = ax.twinx()
    ax_errors.plot(errors_counts['time'], errors_counts['error_count'],
                   label="Liczba błędów", color="black",
                   linestyle='--', linewidth=1,
                   marker='x', markersize=5, mec='black')


    ax_errors.set_ylabel('Liczba błędów')

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2)
    ax_errors.set_ylim(bottom=0)

plt.show()
