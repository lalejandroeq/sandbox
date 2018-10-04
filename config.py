import json


def get_json_object(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data
