import numpy as np
from matplotlib import pyplot as plt

from vizualization.utils.const import error_codes, services_names, charts_dir
from vizualization.utils.load import get_dataframe
from vizualization.utils.utils import get_confidence

path_base = "./../../results"

services = ['flask', 'fastapi', 'flask_5w', 'fastapi_5w', 'spring', 'gin']
iter = [1, 2, 3, 4, 5]
endpoint = "hello"
duration = 120
services_rps_tab = {
    'spring': list(range(100, 801, 100)),
    'gin': list(range(100, 801, 100)),
    'fastapi': list(range(100, 1001, 100)),
    'flask': list(range(100, 901, 100)),
    'fastapi_5w': list(range(100, 1401, 100)),
    'flask_5w': list(range(100, 1401, 100)),
}


fig, axs = plt.subplots(3, 2, figsize=(10, 10), sharex=True,  sharey=True)

for idx, service in enumerate(services):
    ok_means, http_timeout_means, tcp_timeout_means, tcp_reset_means, drop_means = [], [], [], [], []
    ok_confidences, http_timeout_confidences, tcp_timeout_confidences, tcp_reset_confidences, drop_confidences = [], [], [], [], []
    rps_values = services_rps_tab[service]

    for rps in rps_values:
        ok_counts, http_timeout_counts, tcp_timeout_counts, tcp_reset_counts, drop_counts = [], [], [], [], []

        for i in iter:
            try:
                df = get_dataframe(f'const_rps/iter_{i}', service, endpoint, duration, rps, force_process=False)
                error_counts = df['error'].value_counts()

                ok_counts.append(error_counts.get('0', 0))
                http_timeout_counts.append(error_counts.get('1050', 0))
                tcp_timeout_counts.append(error_counts.get('1211', 0))
                tcp_reset_counts.append(error_counts.get('1220', 0))
                drop_counts.append(error_counts.get('drop', 0))
            except:
                pass

        ok_mean = np.mean(ok_counts)
        http_timeout_mean = np.mean(http_timeout_counts)
        tcp_timeout_mean = np.mean(tcp_timeout_counts)
        tcp_reset_mean = np.mean(tcp_reset_counts)
        drop_mean = np.mean(drop_counts)

        ok_confidence = get_confidence(len(ok_counts), ok_mean, np.std(ok_counts))
        http_timeout_confidence = get_confidence(len(http_timeout_counts), http_timeout_mean,
                                                 np.std(http_timeout_counts))
        tcp_timeout_confidence = get_confidence(len(tcp_timeout_counts), tcp_timeout_mean, np.std(tcp_timeout_counts))
        tcp_reset_confidence = get_confidence(len(tcp_reset_counts), tcp_reset_mean, np.std(tcp_reset_counts))
        drop_confidence = get_confidence(len(drop_counts), drop_mean, np.std(drop_counts))

        ok_means.append(ok_mean)
        http_timeout_means.append(http_timeout_mean)
        tcp_timeout_means.append(tcp_timeout_mean)
        tcp_reset_means.append(tcp_reset_mean)
        drop_means.append(drop_mean)

        ok_confidences.append(ok_confidence)
        http_timeout_confidences.append(http_timeout_confidence)
        tcp_timeout_confidences.append(tcp_timeout_confidence)
        tcp_reset_confidences.append(tcp_reset_confidence)
        drop_confidences.append(drop_confidence)


    labels = ['0', '1050', '1211', '1220', 'drop']
    descriptions = [error_codes[label]['desc'] for label in labels]
    colors = [error_codes[label]['color'] for label in labels]


    ax = axs[idx // 2, idx % 2]
    for jdx, label in enumerate(labels):
        means = [ok_means, http_timeout_means, tcp_timeout_means, tcp_reset_means, drop_means][jdx]
        confidences = [ok_confidences, http_timeout_confidences, tcp_timeout_confidences, tcp_reset_confidences, drop_confidences][jdx]
        ax.errorbar(rps_values, means, yerr=confidences, label=descriptions[jdx],
                    fmt='o', color=colors[jdx],
                    linestyle='--', linewidth=0.8, capsize=5)

    ax.set_title(services_names[service])
    ax.grid(True)

    if idx == 0:
        ax.legend()







plt.subplots_adjust(left=0.1, right=0.98, top=0.96, bottom=0.08, hspace=0.13, wspace=0.05)

fig.text(0.5, 0.02, 'Obciążenie RPS', ha='center', fontsize=11)
fig.text(0.015, 0.5, 'Liczba odpowiedzi', va='center', rotation='vertical', fontsize=11)


fig.savefig(f'{charts_dir}/errors_by_rps_and_service_{endpoint}_{duration}.svg', format='svg')

plt.show()
