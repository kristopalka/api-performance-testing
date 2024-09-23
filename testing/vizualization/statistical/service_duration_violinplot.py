import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import to_rgb

from vizualization.utils.const import services_colors, charts_dir
from vizualization.utils.load import get_dataframe

iterations = [1, 2, 3, 4, 5]
services = ['spring'] # 'gin', 'spring', 'fastapi_5w', 'fastapi', 'flask', 'flask_5w'
endpoint = "hello"
duration = 120

services_rps_tab = {
    'spring': list(range(10, 151, 20)) + list(range(200, 500, 50)),
    'gin': list(range(50, 601, 50)),
    'fastapi': list(range(100, 801, 100)),
    'flask': list(range(100, 901, 100)),
    'fastapi_5w': list(range(100, 1401, 100)),
    'flask_5w': list(range(100, 1201, 100)),
}

warmup_time = 20

metric = "duration"
show_errors = False
batch_size = duration - warmup_time


def calculate_params(rps):
    frames = []

    for i in iterations:
        df = get_dataframe(f'const_rps/iter_{i}', service, endpoint, duration, rps)
        measure_df = df[(df['time'] >= warmup_time) & (df['error'] == "0")]
        frames.append(measure_df[['duration']])

    full_df = pd.concat(frames)

    # full_df = full_df[full_df['duration'] < 8]

    return full_df['duration'].values


for service in services:
    rps_tab = services_rps_tab[service]

    results = []
    for rps in rps_tab:
        df = calculate_params(rps)
        results.append(df)


    def darken_color(color, factor=0.7):
        return tuple(np.clip(np.array(to_rgb(color)) * factor, 0, 1).astype(float))


    plt.figure(figsize=(10, 6))
    inner_kws = dict(box_width=7, whis_width=0, color="black", alpha=1)

    ax = sns.violinplot(results, log_scale=True, inner="quart", split=True,
                        color=services_colors[service],
                        linecolor="black", linewidth=0.8,
                        width=0.9,
                        density_norm="area", fill=True)
    ax.set_xticklabels(rps_tab)





    # fig, ax = plt.subplots(figsize=(10, 6))
    # violin_parts = sns.violinplot(results, positions=rps_tab, widths=int(rps_tab[-1]/20),
    #                              points=100,
    #                              showextrema=True, showmedians=True)
    #
    # for pc in violin_parts['bodies']:
    #     pc.set_facecolor(services_colors[service])
    #     pc.set_edgecolor(services_colors[service])
    #     pc.set_alpha(0.5)
    #
    # violin_parts['cmedians'].set_color(services_colors[service])
    #
    # for part in [violin_parts['cbars'], violin_parts['cmins'], violin_parts['cmaxes'], violin_parts['cmedians']]:
    #     part.set_color("black")
    #     part.set_linewidths(1)

    ax.set_yscale("log")
    ax.grid(axis='y')
    ax.set_axisbelow(True)


    ax.set_xlabel('Obciążęnie RPS')
    ax.set_ylabel('Czas odpowiedzi [ms]')

    plt.subplots_adjust(left=0.08, bottom=0.1, right=0.96, top=0.96)
    plt.savefig(
        f'{charts_dir}/service_duration_violinplot/service_duration_violinplot_{service}_{metric}_{endpoint}_{duration}.svg',
        format='svg')

    plt.show()
