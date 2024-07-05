import json


def load_results(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def load_raw(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.readlines()
        return [json.loads(line) for line in raw_data]

