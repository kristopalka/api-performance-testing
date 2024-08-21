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

metrics_colors = {
    "sending": "lightblue",
    "waiting": "blue",
    "receiving": "lightgreen",
    "duration": "blue",
    "connecting": "red",
}

metrics_alpha = {
    "sending": 0.6,
    "waiting": 0.6,
    "receiving": 0.6,
    "duration": 1,
    "connecting": 1,
}
metrics_marker = {
    "sending": "^",
    "waiting": "s",
    "receiving": "v",
    "duration": "o",
    "connecting": ".",
}


error_codes = {
    '0': {'desc': 'HTTP 200', 'color': 'green'},
    '1050': {'desc': 'HTTP request timeout', 'color': 'orange'},
    '1220': {'desc': 'TCP reset by peer', 'color': 'red'},  # read: reset by peer
    '1211': {'desc': 'TCP dial timeout', 'color': 'purple'},  # dial: i/o timeout
    'drop': {'desc': 'Dropped iterations', 'color': 'black'},
}
