from matplotlib import pyplot as plt

from vizualization.utils.const import error_codes, charts_dir
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_error_codes_counts

executor = "ramping_rps"
services = ["gin"] # , "fastapi", "spring", "gin"
endpoint = "hello"
duration = 60
start_rps = 1
end_rps = 4096

time_start = 0
time_stop = duration
top_limit = 4500

rps = f'{start_rps}' if executor == "const_rps" else f'{start_rps}_{end_rps}'
end_rps = start_rps if executor == "const_rps" else end_rps

for service in services:
    df = get_dataframe(executor, service, endpoint, duration, rps)





    df['time'] = df['time'] + 0.58
    df['time'] = df['time'].astype(int)
    error_counts = (df.groupby(['time', 'error']).size().unstack(fill_value=0)
                    .reindex(range(time_start, time_stop), fill_value=0)
                    .reset_index().rename(columns={'index': 'time'}))

    errors_counts = get_error_codes_counts(df)
    for error, props in error_codes.items():
        if error in error_counts.columns:
            print(f"{props['desc']} = {errors_counts[error]['count']}")

    error_counts['rps'] = start_rps + (error_counts['time'] - time_start) * (end_rps - start_rps) / duration


    fig, ax = plt.subplots(figsize=(10, 6))
    for error, props in error_codes.items():
        if error in error_counts.columns:
            ax.plot(error_counts['time'], error_counts[error],
                    label=f"{props['desc']}",
                    color=props['color'])

    ax.plot(error_counts['time'], error_counts['rps'],
            label="Oczekiwana liczba żądań", color='lightblue',
            linestyle='--', linewidth=1.5)

    # ax.set_title(f'service={service}, endpoint={endpoint}, {executor}=({rps}), duration={duration}')
    ax.set_xlabel('Czas od rozpoczęcia eksperymentu [sekundy]')
    ax.set_ylabel('Liczba żądań')

    ax.grid(True)
    ax.set_ylim(top=top_limit, bottom=0)
    ax.set_xlim(left=time_start, right=time_stop)

    ax.legend(loc='upper left')


    plt.subplots_adjust(left=0.08, bottom=0.1,  right=0.96, top=0.96)
    fig.savefig(f'{charts_dir}/time_distribution_errors_counts/time_distribution_errors_counts_{service}_{endpoint}_{duration}_{rps}.svg', format='svg')
    plt.show()
