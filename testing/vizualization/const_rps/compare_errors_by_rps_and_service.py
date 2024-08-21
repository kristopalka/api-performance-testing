import matplotlib.pyplot as plt

from vizualization.utils.const import services_colors_light, services_colors, charts_dir
from vizualization.utils.load import load_results_by_path

path_base = "./../../results"
method = "const_rps"

service_values = ['flask', 'fastapi', 'spring', 'gin']
endpoint = "hello"
duration = 120
# '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192'
rps_values = ['32', '64', '128', '256', '512', '1024']

paths = {
    f'{service}_{rps}rps': f'{path_base}/{method}/{service}/{endpoint}/results_{duration}s_{rps}rps.json'
    for rps in rps_values
    for service in service_values
}

data = {tech: load_results_by_path(path) for tech, path in paths.items()}
failed_requests = {tech: data[tech]['metrics']['http_req_failed']['passes'] for tech in paths.keys()}
success_requests = {tech: data[tech]['metrics']['http_req_failed']['fails'] for tech in paths.keys()}
dropped_iterations = {tech: data[tech]['metrics'].get('dropped_iterations', {}).get('count', 0) for tech in
                      paths.keys()}


# Drawing chart
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.22
number_of_categories = len(rps_values)
number_of_bars = len(service_values)

category_width = bar_width * number_of_categories

for i in range(number_of_bars):
    service = service_values[i]

    pos_x = [category + (i - 1.5) * bar_width for category in range(number_of_categories)]
    failed_counts = [failed_requests[f'{service}_{rps}rps'] for rps in rps_values]
    success_counts = [success_requests[f'{service}_{rps}rps'] for rps in rps_values]
    dropped_counts = [dropped_iterations[f'{service}_{rps}rps'] for rps in rps_values]


    sum_success_fails = [x + y for x, y in zip(failed_counts, success_counts)]

    ax.bar(pos_x, success_counts, bar_width, label=f'{service} HTTP 200', color=services_colors_light[service])
    ax.bar(pos_x, failed_counts, bar_width, label=f'{service} error', bottom=success_counts, color=services_colors[service])
    ax.bar(pos_x, dropped_counts, bar_width, bottom=sum_success_fails, color='gray')

ax.bar(0, 0, 0, label='opuszczone iteracje', color='gray')

ax.set_xlabel('Liczba rps')
ax.set_ylabel('Liczba wysłanych żądań')
ax.set_title(f'Liczba ządań obsłużonych i odrzuconych\nendpoint={endpoint}, duration={duration}')
ax.set_xticks(range(number_of_categories))
ax.set_xticklabels(rps_values)
ax.legend()

# plt.yscale("log")

plt.tight_layout()
plt.show()

fig.savefig(f'{charts_dir}/compare_errors_by_rps_and_service.svg', format='svg')
