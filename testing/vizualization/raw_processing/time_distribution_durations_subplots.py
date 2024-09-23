import pandas as pd
from matplotlib import pyplot as plt

from vizualization.utils.const import services_colors, charts_dir, services_names
from vizualization.utils.load import get_dataframe

executor = "const_rps/iter_1"
services = ["flask", "fastapi", "spring", "gin"]
endpoint = "hello"
duration = 120
rps = 100

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 9), sharex=True, sharey=True)

for idx, service in enumerate(services):
    ax = axs[idx // 2, idx % 2]
    df = get_dataframe(executor, service, endpoint, duration, rps, force_process=False)

    df['time'] = df['time'].astype(int)
    result = df.groupby('time').apply(
        lambda x: pd.Series({
            'mean': x.loc[x['error'] == "0", 'duration'].mean(),
            'std': x.loc[x['error'] == "0", 'duration'].std(),
            'error_count': (x.loc[x['error'] != "0"].shape[0] / x.shape[0]) * 100
        })
    ).reset_index()

    ax.plot(result['time'], result['mean'],
            label="Średni czad odpowiedzi", color=services_colors[service],
            linestyle='-', linewidth=0.8, marker="o", markersize=3)

    ax.fill_between(result['time'],
                    result['mean'] - result['std'],
                    result['mean'] + result['std'],
                    color=services_colors[service], alpha=0.2)

    ax.set_title(services_names[service])

    ax.grid(True)
    ax.set_ylim(bottom=0, top=15)





plt.subplots_adjust(left=0.06, right=0.98, top=0.96, bottom=0.08, hspace=0.10, wspace=0.05)

fig.text(0.5, 0.02, 'Czas od rozpoczęcia eksperymentu [s]', ha='center', fontsize=11)
fig.text(0.015, 0.5, 'Czas odpowiedzi [ms]', va='center', rotation='vertical', fontsize=11)
fig.savefig(f'{charts_dir}/time_distribution_durations/multiple_service_time_distribution_durations_{endpoint}_{duration}_{rps}.svg',
            format='svg')
plt.show()
