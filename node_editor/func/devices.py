import os
import json

from db.redis_db import redis_manager


def upload_devices(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding="utf-8") as file:
                data = json.load(file)
                name = str(data.get('name')) + '_' + str(data.get('id'))
                redis_manager.set(key=name, data=data)
