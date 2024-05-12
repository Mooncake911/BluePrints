DEVICES_NAMES = {}
NODE_IMPORTS = {}


def write_devices_names(names):
    global DEVICES_NAMES
    DEVICES_NAMES = names


def write_node_imports(imports):
    global NODE_IMPORTS
    NODE_IMPORTS = imports


def get_device_name():
    return DEVICES_NAMES


def get_node_imports():
    return NODE_IMPORTS
