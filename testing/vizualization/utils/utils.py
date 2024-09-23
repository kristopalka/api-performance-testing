import numpy as np
from scipy.stats import t, norm


def get_error_codes_counts(df):
    return {
        '0': {'count': (df['error'] == '0').sum()},
        '1211': {'count': (df['error'] == '1211').sum()},
        '1050': {'count': (df['error'] == '1050').sum()},
        '1220': {'count': (df['error'] == '1220').sum()},
        'drop': {'count': (df['error'] == 'drop').sum()}
    }


def get_confidence(number, mean, std):
    d = number - 1  # stopnie swobody (degrees of freedom)
    alpha = 0.05  # poziom istotności
    t_critical = t.ppf(1 - alpha / 2, d)  # wartość krytyczna t

    margin_of_error = t_critical * (std / np.sqrt(number))

    confidence_interval = (mean - margin_of_error, mean + margin_of_error)
    return margin_of_error
