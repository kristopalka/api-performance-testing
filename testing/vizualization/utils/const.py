charts_dir = './../../charts'

services_colors = {
    'spring': 'tab:green',
    'fastapi': 'tab:red',
    'flask': 'tab:orange',
    'gin': 'tab:blue'
}

services_colors_light = {
    'spring': '#6bbc6b',
    'fastapi': '#e26868',
    'flask': '#ffa556',
    'gin': '#62a0cb'
}


error_codes = {
    0: {'desc': 'HTTP 200', 'color': 'blue'},
    1: {'desc': 'Dropped iterations', 'color': 'green'},
    1211: {'desc': 'Dial: i/o timeout', 'color': 'orange'},
    1050: {'desc': 'Request timeout', 'color': 'purple'},
    1220: {'desc': 'Read: reset by peer', 'color': 'red'}
}