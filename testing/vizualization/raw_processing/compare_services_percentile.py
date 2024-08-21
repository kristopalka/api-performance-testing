import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from vizualization.utils.const import *
from vizualization.utils.load import get_dataframe

executor = "const_rps"

services = ["flask", "fastapi", "spring", "gin"]
endpoint = "hello"
percentiles = [x / 100.0 for x in range(0, 101, 1)]

metric = "duration"
duration = 120
rps_tab = list(range(10, 101, 10))
warmup_time = 20
show_errors = True


def calculate_for_service(service):
    dfs = {rps: get_dataframe(executor, service, endpoint, duration, rps) for rps in rps_tab}

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

plt.figure(figsize=(12, 8))
for index, row in results_df.iterrows():
    print(f'{row['service']}: {row['error_rate']}')

    plt.plot(row[percentiles_str], percentiles,
             marker='o', markersize=0,
             color=services_colors[row['service']], label=row['service'])

plt.xscale('log')
plt.xlabel('Czas odpowiedzi [ms]')
plt.ylabel('Percentyl')
plt.title(f'Percentyle czasu odpowiedzi http_req_{metric} dla endpointu \\{endpoint}, duration={duration}, warmup_time={warmup_time}')
plt.legend()
plt.grid(True, which='both', linestyle='-', linewidth=0.5)
plt.show()
