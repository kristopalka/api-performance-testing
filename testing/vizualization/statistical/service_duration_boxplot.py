import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb

from vizualization.utils.const import services_colors, charts_dir
from vizualization.utils.load import get_dataframe

iterations = [1, 2, 3, 4, 5]
services = ["spring", "gin", "flask", "fastapi", "flask_5w", "fastapi_5w"]  # "spring", "gin", "flask", "fastapi", "flask_5w", "fastapi_5w"
endpoint = "hello"
duration = 120

services_rps_tab = {
    'spring': list(range(10, 151, 10)),
    'gin': list(range(50, 701, 50)),
    'fastapi': list(range(50, 801, 50)),
    'flask': list(range(50, 901, 50)),
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

    return full_df['duration'].values


for service in services:
    rps_tab = services_rps_tab[service]

    results = []
    for rps in rps_tab:
        df = calculate_params(rps)

        results.append(df)

    fig, ax = plt.subplots(figsize=(10, 6))

    linewidth = 1
    boxwidth = (rps_tab[-1] - rps_tab[0]) / len(rps_tab) * 0.8

    flierprops = dict(markerfacecolor="black", markersize=2, marker=".", markeredgewidth=0)
    medianprops = dict(color="black", linewidth=linewidth)
    boxprops = dict(linewidth=linewidth)
    whiskerprops = dict(linewidth=linewidth)
    capprops = dict(linewidth=linewidth)

    boxplot = ax.boxplot(results, patch_artist=True, widths=boxwidth,
                         labels=rps_tab, positions=rps_tab,
                         flierprops=flierprops, medianprops=medianprops,
                         boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops)

    # zmiana koloru tła boxplot
    for patch in boxplot['boxes']:
        rgb_values = to_rgb(services_colors[service]) + (0.8,)
        patch.set_facecolor(rgb_values)

    # losowe rozłożenie fliers i usuwanie częsci
    to_remove_fliers = 0
    num_of_fliers = 0
    prev_max_label_y = 200
    for i in range(len(results)):
        flier_data = boxplot['fliers'][i].get_ydata()
        x_vals = boxplot['fliers'][i].get_xdata()

        num_of_fliers += len(flier_data)

        num_to_remove = int(len(flier_data) * to_remove_fliers)
        indices_to_remove = np.random.choice(len(flier_data), size=num_to_remove, replace=False)

        # # keep bigest value
        # max_flier_index = np.argmax(flier_data)
        # if max_flier_index in indices_to_remove:
        #     index = np.where(indices_to_remove == max_flier_index)[0]
        #     array = np.delete(indices_to_remove, index)


        filtered_fliers = np.delete(flier_data, indices_to_remove)
        filtered_x_vals = np.delete(x_vals, indices_to_remove)

        margin = boxwidth * 0.5
        x_vals_random = filtered_x_vals + np.random.uniform(-margin, margin, size=len(filtered_fliers))

        plt.setp(boxplot['fliers'][i], ydata=filtered_fliers, xdata=x_vals_random)


        def format_number(num):
            return f"{num:.3g}" if num >= 1e-3 and num <= 1e3 else f"{num:.4g}"

        # Dodawanie podpisów
        flier_percentage = round(len(flier_data) / len(results[i]) * 100, 2)
        y = max(prev_max_label_y, results[i].max(), 1.5 * boxplot['whiskers'][i * 2 + 1].get_ydata()[1])
        prev_max_label_y = max(y, prev_max_label_y)

        ax.text(rps_tab[i], y, f'{format_number(flier_percentage)}%', ha='center', va='bottom', size=9)

    # fliers label
    #ax.scatter([], [], label=f'Losowo wybrane {round((1 - to_remove_fliers) * 100)}% pomiarów odstających', c="black",
    #            s=5, marker='.')

    ax.set_yscale("log")
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    ax.grid(True)

    ax.set_xlabel('Obciążęnie RPS')
    ax.set_ylabel('Czas odpowiedzi [ms]')
    plt.subplots_adjust(left=0.07, bottom=0.1, right=0.97, top=0.96)


    plt.legend(loc="upper left")
    plt.show()

    fig.savefig(
        f'{charts_dir}/service_duration_boxplot/{service}_{metric}_{endpoint}_{duration}.svg',
        format='svg')
