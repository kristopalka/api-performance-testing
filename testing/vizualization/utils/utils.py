import math


def round_significant_digits(number, digits=3):
    if number == 0:
        return 0

    digits_before_decimal = math.floor(math.log10(abs(number))) + 1
    rounded_number = round(number, digits - digits_before_decimal)
    return rounded_number


colors = {
    'spring': 'tab:green',
    'fastapi': 'tab:red',
    'flask': 'tab:orange',
    'gin': 'tab:blue'
}

colors_light = {
    'spring': '#6bbc6b',
    'fastapi': '#e26868',
    'flask': '#ffa556',
    'gin': '#62a0cb'
}
