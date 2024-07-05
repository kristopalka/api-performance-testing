import matplotlib.pyplot as plt

from vizualization.utils.utils import load_data

service_values = ['spring', 'fastapi', 'flask', 'gin']
service_colors = ['tab:green', 'tab:red', 'tab:orange', 'tab:blue']
endpoint = "hello"
duration = 15
vus_values = ['128', '256', '512', '1024', '2048', '4096', '8192', '16384', '32768']
metric = "http_req_failed"
param = "passes"

path_base = "./../results"
paths = {
    f'{service}_{vus}vus': f'{path_base}/{service}/{endpoint}/results_{duration}s_{vus}vus.json'
    for vus in vus_values
    for service in service_values
}

data = {tech: load_data(path) for tech, path in paths.items()}
params = {tech: data[tech]['metrics'][metric][param] for tech in paths.keys()}

# Drawing chart
fig, ax = plt.subplots()

bar_width = 0.2
number_of_categories = len(vus_values)
number_of_bars = len(service_values)

category_width = bar_width * number_of_categories

for i in range(number_of_bars):
    positions_x = [category + (i - 1.5) * bar_width for category in range(number_of_categories)]
    counts = [params[f'{service_values[i]}_{vus}vus'] for vus in vus_values]
    bar = ax.bar(positions_x, counts, bar_width, label=service_values[i], color=service_colors[i])

ax.set_xlabel('Liczba vus')
ax.set_ylabel('Liczba żądań')
ax.set_title(f'Liczba ządań udrzuconych ({metric}) dla endpointu /{endpoint}\nendpoint={endpoint}, duration={duration}')
ax.set_xticks(range(number_of_categories))
ax.set_xticklabels(vus_values)
ax.legend()

plt.tight_layout()
plt.show()
