from matplotlib import pyplot as plt
from vizualization.utils.const import error_codes, charts_dir

from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_error_codes_counts

executor = "ramping_rps"
service = "fastapi"
endpoint = "hello"
duration = 150
start_rps = 32
end_rps = 16384

df = get_dataframe(executor, service, endpoint, duration, f'{start_rps}_{end_rps}')
errors_counts = get_error_codes_counts(df)

df['time'] = df['time'].astype(int)
error_distribution_counts = df.groupby(['time', 'error']).size().unstack(fill_value=0)

time_index = range(int(df['time'].min()), int(df['time'].max()) + 1)
error_distribution_counts = error_distribution_counts.reindex(time_index, fill_value=0).reset_index().rename(columns={'index': 'time'})

fig, ax = plt.subplots(figsize=(14, 8))

for error, props in error_codes.items():
    if error in error_distribution_counts.columns:
        plt.plot(error_distribution_counts['time'], error_distribution_counts[error],
                 label=f"{props['desc']} ({errors_counts[error]['count']})",
                 color=props['color'])

ax.set_title(f'Ilość wystąpień błędów w każdej sekundzie dla {service}'
                  f'endpoint={endpoint}, start_rps={start_rps}, end_rps={end_rps}, duration={duration}')
ax.set_xlabel('Czas od rozpoczęcia eksperymentu (sekundy)')
ax.set_ylabel('Ilość wystąpień odpowiedzi każdego typu')
ax.grid(True)
ax.set_xlim(left=0)
ax.legend(loc='upper left')


ax_line = ax.twinx()
ax_line.plot([0, duration], [start_rps, end_rps],
             label="Ilość wysyłanych żadań",
             color='lightblue', linestyle='-',linewidth=2)
ax_line.set_ylabel('Ilość wysyłanych żądań na sekundę (RPS)')
ax_line.set_ylim(top=2 * end_rps)
ax_line.legend(loc='upper right')


fig.savefig(f'{charts_dir}/responses_distribution_counts_{service}_{duration}s_{start_rps}_{end_rps}.png', format='png')
plt.show()
