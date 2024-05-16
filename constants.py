import json


DEVICES_NAMES = {}


def set_devices_names_to_default():
    global DEVICES_NAMES
    DEVICES_NAMES = {}


def string_to_dict(line: str):
    start_index = line.find('{')
    end_index = line.rfind('}')

    # Check if { and } were found
    if start_index != -1 and end_index != -1:
        json_str = line[start_index:end_index + 1]

        try:
            json_dict = json.loads(json_str)
            return json_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON {e}")

    else:
        return None


def add_device_config(data: str):
    global DEVICES_NAMES
    data = string_to_dict(data)
    if data and data.get('id') and data.get('name'):
        name = data.get("name")
        DEVICES_NAMES[name] = data


def get_devices_names():
    global DEVICES_NAMES
    return DEVICES_NAMES


NODE_IMPORTS = {}


def write_node_imports(imports):
    global NODE_IMPORTS
    NODE_IMPORTS = imports


def get_node_imports():
    global NODE_IMPORTS
    return NODE_IMPORTS
