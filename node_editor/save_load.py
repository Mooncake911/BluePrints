import json

from PySide6 import QtCore

from .connection import Connection
from .node import Node
from .pin import Pin


def load_scene(scene, json_path, imports):
    """ Load the scene from the json file """

    with open(json_path) as f:
        data = json.load(f)

    # clear out the python_node_interface lookup
    node_lookup = {}  # A dictionary of nodes, by uuids for faster looking up. Refactor this in the future

    if data:

        # Add the nodes
        for n in data["nodes"]:
            info = imports[n["type"]]
            node = info["class"]()
            node.uuid = n["uuid"]
            node.value = n["value"]
            pos = QtCore.QPointF(n["x"], n["y"])

            scene.addItem(node)
            node.init_widget()
            node.build()
            node.setPos(pos)
            # self.create_node(node, pos)

            node_lookup[node.uuid] = node

        # Add the connections
        for c in data["connections"]:
            start_pin = node_lookup[c["start_uuid"]].get_pin(c["start_pin"])
            end_pin = node_lookup[c["end_uuid"]].get_pin(c["end_pin"])

            connection = Connection(None)
            scene.addItem(connection)

            if start_pin:
                connection.set_start_pin(start_pin)
            if end_pin:
                connection.set_end_pin(end_pin)

            connection.update_start_and_end_pos()


def save_scene(scene, json_path):
    """ Save the scene to the json file """

    json_scene = {"nodes": [], "connections": []}

    for item in scene.items():

        # Nodes
        if isinstance(item, Node):
            pos = item.pos().toPoint()
            obj_type = type(item).__name__

            node = {
                "type": obj_type,
                "x": pos.x(),
                "y": pos.y(),
                "uuid": str(item.uuid),
                "value": item.value,
            }

            json_scene["nodes"].append(node)

        # Connections
        if isinstance(item, Connection):

            connection = {
                "start_uuid": str(item.start_pin.node.uuid),
                "end_uuid": str(item.end_pin.node.uuid),
                "start_pin": item.start_pin.name,
                "end_pin":  item.end_pin.name,
            }

            json_scene["connections"].append(connection)
            continue

        # Pins
        if isinstance(item, Pin):
            # Future code
            continue

    with open(json_path, "w") as f:
        json.dump(json_scene, f, indent=4)
