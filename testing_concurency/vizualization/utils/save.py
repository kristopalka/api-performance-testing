from vizualization.utils.const import charts_dir


def save_to_pdf(fig, name):
    fig.savefig(f'{charts_dir}/{name}.pdf', format='pdf')
