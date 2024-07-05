import matplotlib.pyplot as plt

from vizualization.utils.utils import load_data

params = ['avg', 'min', 'p(10)', 'p(20)', 'p(30)', 'p(40)', 'med', 'p(60)', 'p(70)', 'p(80)', 'p(90)', 'p(95)', 'p(98)','p(99)', 'p(99.9)', 'max']
endpoint = "hello"
metric = "http_req_duration"

path_base = "./../results"
paths = {
    'spring_1024vus': f'{path_base}/spring/results_{endpoint}_15s_1024vus.json',
    'fastapi_1024vus': f'{path_base}/fastapi/results_{endpoint}_15s_1024vus.json',
}

data = {tech: load_data(path) for tech, path in paths.items()}

durations = {tech: [data[tech]['metrics'][metric][param] for param in params] for tech in paths.keys()}

fig, ax = plt.subplots()

x = range(len(params))
bar_width = 0.4

i = 0
for key in paths:
    ax.bar([p + i * bar_width for p in x], durations[key], bar_width, label=key)
    i += 1

ax.set_xlabel('Parametry')
ax.set_ylabel('Czas odpowiedzi (ms)')
ax.set_title(f'{metric} dla endpointu /{endpoint}')
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels(params)
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
