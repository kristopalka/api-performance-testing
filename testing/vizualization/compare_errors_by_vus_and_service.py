import matplotlib.pyplot as plt

from vizualization.utils.utils import colors, colors_light, round_significant_digits, load_data

path_base = "./../results"

service_values = ['spring', 'fastapi', 'flask', 'gin']
endpoint = "hello"
duration = 15
vus_values = ['128', '256', '512', '1024', '2048', '4096', '8192', '16384', '32768']
metric = "http_req_failed"

paths = {
    f'{service}_{vus}vus': f'{path_base}/{service}/{endpoint}/results_{duration}s_{vus}vus.json'
    for vus in vus_values
    for service in service_values
}

data = {tech: load_data(path) for tech, path in paths.items()}
failed_requests = {tech: data[tech]['metrics'][metric]['passes'] for tech in paths.keys()}
success_requests = {tech: data[tech]['metrics'][metric]['fails'] for tech in paths.keys()}

# Drawing chart
fig, ax = plt.subplots()

bar_width = 0.22
number_of_categories = len(vus_values)
number_of_bars = len(service_values)

category_width = bar_width * number_of_categories

for i in range(number_of_bars):
    service = service_values[i]

    pos_x = [category + (i - 1.5) * bar_width for category in range(number_of_categories)]
    failed_counts = [failed_requests[f'{service}_{vus}vus'] for vus in vus_values]
    success_counts = [success_requests[f'{service}_{vus}vus'] for vus in vus_values]

    ax.bar(pos_x, success_counts, bar_width, label=service, color=colors_light[service])
    ax.bar(pos_x, failed_counts, bar_width, bottom=success_counts, color=colors[service])

    for j in range(number_of_categories):
        if failed_counts[j] != 0:
            requests_num = failed_counts[j] + success_counts[j]
            rate = round_significant_digits(100 * failed_counts[j] / requests_num, 3)
            ax.text(pos_x[j] + bar_width / 15, 50000, f'{rate}%', ha='center', va='bottom', rotation=90, fontsize=7)

ax.set_xlabel('Liczba vus')
ax.set_ylabel('Liczba wysłanych żądań')
ax.set_title(
    f'Liczba ządań obsłużonych i odrzuconych oraz % odrzuconych\nendpoint={endpoint}, duration={duration}')
ax.set_xticks(range(number_of_categories))
ax.set_xticklabels(vus_values)
ax.legend()

plt.tight_layout()
plt.show()

fig.savefig('compare_errors_by_vus_and_service.svg', format='svg')
