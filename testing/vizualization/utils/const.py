charts_dir = './../../charts'

services_colors = {
    'spring': '#3a923a',
    'fastapi': '#c03d3e',
    'fastapi_5w': '#9372b2',
    'flask': '#e1812c',
    'flask_5w': '#845b53',
    'gin': '#3274a1'
}

gray = "#3d3d3d"

services_names = {
    'spring': 'Spring',
    'fastapi': 'FastAPI',
    'fastapi_5w': 'FastAPI 5w',
    'flask': 'Flask',
    'flask_5w': 'Flask 5w',
    'gin': 'Gin'
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
    '0': {'desc': 'Kod HTTP 200', 'color': 'green'},
    '1050': {'desc': 'Przekroczenie czasu HTTP', 'color': 'orange'},
    '1220': {'desc': 'Reset połączenia TCP', 'color': 'red'},  # read: reset by peer
    '1211': {'desc': 'Przekroczenie czasu TCP', 'color': 'purple'},  # dial: i/o timeout
    'drop': {'desc': 'Odrzucona iteracja', 'color': 'black'},
}
