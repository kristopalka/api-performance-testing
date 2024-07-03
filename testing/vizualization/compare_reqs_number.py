import matplotlib.pyplot as plt

from vizualization.compare_by_vus import load_data

vus_values = ['128', '256', '512', '1024', '2048']
endpoint = "hello"
metric = "http_reqs"
param = "count"

path_base = "./../results"
paths = {
    f'spring_{vus}vus': f'{path_base}/spring/results_{endpoint}_15s_{vus}vus.json' for vus in vus_values
}
paths.update({
    f'fastapi_{vus}vus': f'{path_base}/fastapi/results_{endpoint}_15s_{vus}vus.json' for vus in vus_values
})



data = {tech: load_data(path) for tech, path in paths.items()}

counts = {tech: data[tech]['metrics'][metric][param] for tech in paths.keys()}

fig, ax = plt.subplots()

techs = list(counts.keys())
counts_values = list(counts.values())

bar_width = 0.35
x = range(len(vus_values))

positions_fastapi = [i - bar_width/2 for i in x]
positions_spring = [i + bar_width/2 for i in x]

counts_fastapi = [counts[f'fastapi_{vus}vus'] for vus in vus_values]
counts_spring = [counts[f'spring_{vus}vus'] for vus in vus_values]

bars_fastapi = ax.bar(positions_fastapi, counts_fastapi, bar_width, label='FastAPI', color='blue')
bars_spring = ax.bar(positions_spring, counts_spring, bar_width, label='Spring', color='green')

ax.set_xlabel('Ilość VUs')
ax.set_ylabel('Liczba żądań (count)')
ax.set_title(f'Liczba żądań ({metric}) dla endpointu /{endpoint}')
ax.set_xticks(x)
ax.set_xticklabels(vus_values)
ax.legend()

plt.tight_layout()
plt.show()