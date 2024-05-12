import os
import json


def upload_devices(folder_path):
    json_data = {}

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding="utf-8") as file:
                data = json.load(file)
                json_data[filename.split('.')[0]] = data

    return json_data
