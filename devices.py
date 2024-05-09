import os
import json


def read_json_files(folder_path):
    json_data = {}

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding="utf-8") as file:
                data = json.load(file)
                json_data[filename.split('.')[0]] = data

    return json_data


if 'DEVICES_NAMES' not in globals():
    DEVICES_NAMES = read_json_files("devices")
