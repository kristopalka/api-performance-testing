from statistics import mean, pstdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from vizualization.utils.const import services_colors, charts_dir, services_names
from vizualization.utils.load import get_dataframe, save_df
from vizualization.utils.utils import get_confidence

iterations = [1, 2, 3, 4, 5]
services = ['spring'] # 'gin', 'spring', 'fastapi_5w', 'fastapi', 'flask', 'flask_5w'
endpoint = "hello"
duration = 120

num_of_batches = 5
warmup_time = 10

services_rps_tab = {
    'spring': list(range(10, 151, 10)) + list(range(200, 501, 50)),
    'gin': list(range(10, 151, 20)) + list(range(200, 701, 50)),
    'fastapi': list(range(50, 801, 50)),
    'flask': list(range(50, 901, 50)),
    'fastapi_5w': list(range(50, 1401, 50)),
    'flask_5w': list(range(50, 1201, 50)),
}

metric = "duration"
show_errors = False
batch_size = duration - warmup_time


def calculate_params(rps):
    durations = []
    errors = []

    for i in iterations:
        df = get_dataframe(f'const_rps/iter_{i}', service, endpoint, duration, rps)
        measure_df = df[(df['time'] >= warmup_time)]

        dfs = np.array_split(measure_df, num_of_batches)
        for i, df_part in enumerate(dfs):
            df_dur = df_part[df_part['error'] == "0"][metric]
            if df_dur.shape[0] > 0:
                dur_mean = df_dur.mean()
                durations.append(dur_mean)

            errors_number = df_part[df_part['error'] != "0"].shape[0]
            error_rate = errors_number / (df_part.shape[0] + errors_number) * 100
            errors.append(error_rate)


    print(f'rps={rps}, durations={durations}, errors={errors}')

    return {
        'key': rps,
        'dur_mean': mean(durations),
        'dur_std': pstdev(durations),
        'dur_conf': get_confidence(len(durations), mean(durations), pstdev(durations)),
        'error_mean': mean(errors),
        'error_std': pstdev(errors),
        'error_conf': get_confidence(len(errors), mean(errors), pstdev(errors))
    }


for service in services:
    rps_tab = services_rps_tab[service]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax_errors = ax.twinx()

    temp_file_name = f'temp_service_duration_by_rps/{service}_durations_by_rps.csv'

    # try:
    #     results_df = read_df(temp_file_name)
    # except:
    results = []
    for rps in rps_tab:
        params = calculate_params(rps)
        results.append(params)

    results_df = pd.DataFrame(results)
    save_df(results_df, temp_file_name)

    print(results_df)



    ax_errors.errorbar(results_df['key'], results_df['error_mean'], yerr=results_df['error_conf'],
                       label=f'Odsetek błędów {services_names[service]}', linestyle='--', linewidth=0.8,
                       ecolor="black", color="black",
                       marker='x', markersize=5,
                       mfc='red', mec='black', capsize=5)

    ax.errorbar(results_df['key'], results_df['dur_mean'], yerr=results_df['dur_conf'],
                label=f'Czas odpowiedzi {services_names[service]}', linestyle='--', linewidth=0.8,
                color=services_colors[service],
                ecolor=services_colors[service],
                marker='o', markersize=5, capsize=5)

    ax.set_xlabel('Obciążęnie RPS')
    ax.set_ylabel('Czas odpowiedzi [ms]')
    # plt.title(
    #     f'service={service}, metric=http_req_{metric}, endpoint={endpoint}, duration={duration}, warmup_time={warmup_time}')

    ax.set_yscale("log")
    ax.set_ylim(bottom=0.1)
    ax.set_xlim(left=0)
    ax.grid(True)

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_errors.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    ax_errors.set_ylim(bottom=0, top=100)
    ax_errors.set_ylabel('Odsetek błędów [%]')

    plt.subplots_adjust(left=0.07, bottom=0.1, right=0.93, top=0.96)
    fig.savefig(f'{charts_dir}/service_duration_and_errors_by_rps/{service}_{endpoint}_{duration}s.svg', format='svg')
    plt.show()
