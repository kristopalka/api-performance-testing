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

fig, ax = plt.subplots(figsize=(14, 8))

for error, group in df.groupby('error'):
    plt.scatter(group['time'], group['duration'],
                label=f"{error_codes[error]['desc']}: {errors_counts[error]['count']}",
                s=5, color=error_codes[error]['color'])

ax.set_title(f'Rozkład odpowiedzi serwisu {service}: '
                  f'endpoint={endpoint}, start_rps={start_rps}, end_rps={end_rps}, duration={duration}')
ax.set_xlabel('Czas w którym wysłano odpowiedź (sekundy)')
ax.set_ylabel('Ile czasu czekano na otrzymanie odpowiedzi lub stwierdzenie błędu (ms)')
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


fig.savefig(f'{charts_dir}/responses_distribution_{service}_{duration}s_{start_rps}_{end_rps}.png', format='png')
plt.show()
