from matplotlib import pyplot as plt

from vizualization.utils.const import error_codes, charts_dir
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_error_codes_counts

executor = "const_rps"
service = "fastapi"
endpoint = "hello"
duration = 120
start_rps = 110
end_rps = start_rps

time_start = 0
time_stop = duration
top_limit = 2000

rps = f'{start_rps}' if executor == "const_rps" else f'{start_rps}_{end_rps}'
end_rps = start_rps if executor == "const_rps" else end_rps

df = get_dataframe(executor, service, endpoint, duration, rps)

errors_counts = get_error_codes_counts(df)


df['time'] = df['time'].astype(int)
error_counts = (df.groupby(['time', 'error']).size().unstack(fill_value=0)
                .reindex(range(time_start, time_stop), fill_value=0)
                .reset_index().rename(columns={'index': 'time'}))



error_counts['rps'] = start_rps + (error_counts['time'] - time_start + 0.5) * (end_rps - start_rps) / duration


fig, ax = plt.subplots(figsize=(14, 8))
for error, props in error_codes.items():
    if error in error_counts.columns:
        ax.plot(error_counts['time'], error_counts[error],
                label=f"{props['desc']} ({errors_counts[error]['count']})",
                color=props['color'])

ax.plot(error_counts['time'], error_counts['rps'],
        label="Liczba wysłanych żądań", color='lightblue',
        linestyle='--', linewidth=1.5)

ax.set_title(f'Liczba błędów próbkowana co sekundę {service} /{endpoint}: '
             f'start_rps={start_rps}, end_rps={end_rps}, duration={duration}')
ax.set_xlabel('Czas od rozpoczęcia eksperymentu (sekundy)')
ax.set_ylabel('Liczba odpowiedzi każdego typu')

ax.grid(True)
ax.set_xlim(left=0)
if top_limit == 0:
    ax.set_ylim(auto=True)
else:
    ax.set_ylim(top=top_limit, bottom=-200)
ax.legend(loc='upper left')

fig.savefig(f'{charts_dir}/responses_distribution_counts_{service}_{endpoint}_{duration}s_{start_rps}_{end_rps}.png', format='png')
plt.show()
