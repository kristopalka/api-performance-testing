import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from vizualization.utils.const import *
from vizualization.utils.load import get_dataframe

executor = "const_rps"

iterations = [1, 2, 3, 4, 5]


services = ["flask", "fastapi", "spring", "gin"]
endpoint = "hello"
percentiles = [x / 200.0 for x in range(0, 201, 1)]

metric = "duration"
duration = 120
start, end, step = 50, 1000, 50
rps_tab = range(start, end + 1, step)
warmup_time = 20
show_errors = True


def calculate_for_service(service):
    dfs = {rps: get_dataframe(f'const_rps/iter_0', service, endpoint, duration, rps) for rps in rps_tab}

    errors_number = sum((df['error'] != "0").sum() for df in dfs.values())
    joined_durations = pd.concat([
        df[(df['time'] >= warmup_time) & (df['error'] == "0")][[metric]]
        for df in dfs.values()
    ], ignore_index=True)

    return {
        'service': service,
        'error_rate': errors_number / (joined_durations.shape[0] + errors_number),
        **{f'{percentile}': joined_durations[metric].quantile(percentile) for percentile in percentiles},
    }


results_df = pd.DataFrame([calculate_for_service(service) for service in services])

percentiles_str = [f'{p}' for p in percentiles]

plt.figure(figsize=(10, 6))
for index, row in results_df.iterrows():
    print(f'{services_names[row['service']]}: {row['error_rate']}')


    plt.plot(row[percentiles_str], percentiles, color=services_colors[row['service']], label=services_names[row['service']],
             markersize=0)


plt.xscale('log')
plt.xlabel('Czas odpowiedzi [ms]')
plt.ylabel('Percentyl czasu odpowiedzi')
# plt.title(
#     f'metric=http_req_{metric}, endpoint={endpoint}, duration={duration}, warmup_time={warmup_time}, range=({start}, {end}, {step})')
plt.legend()
plt.grid(True, which='both', linestyle='-', linewidth=0.5)

# Dodanie małego wykresu słupkowego z błędami
if show_errors:
    plt.rcParams['hatch.linewidth'] = 0.4
    ax_inset = inset_axes(plt.gca(), width="30%", height="30%", loc='lower right', bbox_to_anchor=(0.16, 0.14, 0.8, 0.8),
                          bbox_transform=plt.gcf().transFigure)
    ax_inset.bar([services_names[s] for s in results_df['service']], results_df['error_rate'], color=[services_colors[s] for s in results_df['service']],
                 edgecolor='black', linewidth=0.8, hatch='xxx')
    ax_inset.set_title('Odsetek błędów dla serwisów', fontsize=11)
    ax_inset.set_ylabel('Odsetek błędów [%]', fontsize=10)
    ax_inset.set_ylim(bottom=0)

plt.subplots_adjust(left=0.07, bottom=0.1, right=0.97, top=0.97)
plt.savefig(f'{charts_dir}/distribuant/{endpoint}_{duration}_{start}_{end}_{step}.svg', format='svg')
plt.show()
