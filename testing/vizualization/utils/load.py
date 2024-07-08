import json

import ujson


def load_results(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def load_raw(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.readlines()
        return [json.loads(line) for line in raw_data]

def load_json_by_metric(path, *metrics):
    with open(path, 'r') as file:
        for line in file:
            json_object = ujson.loads(line)
            if json_object['type'] == "Point" and json_object['metric'] in metrics:
                yield json_object
