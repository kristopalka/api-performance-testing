import matplotlib.pyplot as plt

from vizualization.utils.const import services_colors_light
from vizualization.utils.load import load_results_by_path

path_base = "./../../results"
method = "const_rps"

service_values = ['spring', 'fastapi', 'flask', 'gin']
endpoint = "hello"
duration = 120
# '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192'
rps_values = ['32', '64', '128', '256', '512', '1024']
metric_key = 'duration'

paths = {
    f'{service}_{rps}rps': f'{path_base}/{method}/{service}/{endpoint}/results_{duration}s_{rps}rps.json'
    for rps in rps_values
    for service in service_values
}

data = {tech: load_results_by_path(path) for tech, path in paths.items()}
metric_data = {tech: data[tech]['metrics']['http_req_stats']['data']['tags'][metric_key] for tech in paths.keys()}

# Drawing chart
fig, ax = plt.subplots()

bar_width = 0.22
number_of_categories = len(rps_values)
number_of_bars = len(service_values)

category_width = bar_width * number_of_categories

for i in range(number_of_bars):
    service = service_values[i]

    pos_x = [category + (i - 1.5) * bar_width for category in range(number_of_categories)]
    counts = [metric_data[f'{service}_{rps}rps'] for rps in rps_values]

    ax.bar(pos_x, counts, bar_width, label=f'{service}', color=services_colors_light[service])

    # for j in range(number_of_categories):
    #    ax.text(pos_x[j] + bar_width / 1000, 0, f'{counts[j]}', ha='center', va='bottom', rotation=90, fontsize=7)

ax.set_xlabel('Liczba rps')
ax.set_ylabel(f'{metric_key}')
ax.set_title(
    f'Porównanie metryki {metric_key}\nendpoint={endpoint}, duration={duration}')
ax.set_xticks(range(number_of_categories))
ax.set_xticklabels(rps_values)
ax.legend()

plt.yscale("log")

plt.tight_layout()
plt.show()

fig.savefig(f'out/compare_{metric}_{metric_key}_by_rps_and_service.svg', format='svg')
