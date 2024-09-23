from matplotlib import pyplot as plt
from vizualization.utils.const import error_codes, charts_dir
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_error_codes_counts

executor = "const_rps/iter_0"
service = "gin"
endpoint = "hello"
duration = 120
time_start = 0
time_stop = duration


rps_values = [800, 400, 200, 100]


fig, axs = plt.subplots(nrows=len(rps_values), ncols=1, figsize=(10, 10), sharex=True)

for ax, rps in zip(axs, rps_values):
    end_rps = rps


    df = get_dataframe(executor, service, endpoint, duration, rps, force_process=True)
    errors_counts = get_error_codes_counts(df)

    df['time'] = df['time'] + 0.03
    df['time'] = df['time'].astype(int)
    error_counts = (df.groupby(['time', 'error']).size().unstack(fill_value=0)
                    .reindex(range(time_start, time_stop), fill_value=0)
                    .reset_index().rename(columns={'index': 'time'}))

    error_counts['rps'] = rps + (error_counts['time'] - time_start) * (end_rps - rps) / duration

    for error, props in error_codes.items():
        if error in error_counts.columns:
            ax.plot(error_counts['time'], error_counts[error],
                    label=f"{props['desc']}",
                    color=props['color'])

    ax.plot(error_counts['time'], error_counts['rps'],
            label="Oczekiwana liczba żądań", color='lightblue',
            linestyle='--', linewidth=1.5)

    ax.set_ylim(bottom=0, top=int(1.7 * int(rps)))
    ax.set_xlim(left=time_start, right=time_stop)
    ax.grid(True)
    ax.set_ylabel(f'RPS={rps}', fontsize=12)

    if rps == rps_values[0]:
        ax.legend(loc='upper right')





#fig.text(0.5, 0.97, f'service={service}, endpoint={endpoint}, duration={duration}', ha='center', fontsize=13)
fig.text(0.5, 0.02, 'Czas od rozpoczęcia eksperymentu (sekundy)', ha='center', fontsize=12)
fig.text(0.017, 0.5, 'Liczba odpowiedzi', va='center', rotation='vertical', fontsize=12)

plt.subplots_adjust(left=0.11, bottom=0.06, right=0.97, top=0.98, hspace=0.06)
fig.savefig(f'{charts_dir}/time_distribution_errors_counts/multiple_rps_time_distribution_errors_counts_{service}_{endpoint}_{duration}.svg', format='svg')
plt.show()