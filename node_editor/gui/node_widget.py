import json
import uuid

from PySide6 import QtGui, QtWidgets

from .view import View
from .node_editor import NodeEditor
from .node_scene import NodeScene

from ..connection import Connection
from ..node import Node
from ..pin import Pin


class NodeWidget(QtWidgets.QWidget):
    """
    Widget for creating and displaying a python_node_interface editor.

    Attributes:
        node_editor (NodeEditor): The python_node_interface editor object.
        view (View): Отрисовка заднего фона и добавление базового функционала редактора.
        node_scene (NodeScene): Функционал относящийся к виджету Node.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.node_lookup = {}  # A dictionary of nodes, by uuids for faster looking up. Refactor this in the future

        self.node_editor = NodeEditor(self)
        self.node_scene = NodeScene()
        self.node_scene.setSceneRect(0, 0, 9999, 9999)
        self.node_editor.install(self.node_scene)

        self.view = View(self)
        self.view.setScene(self.node_scene)
        self.view.request_node.connect(self.create_node)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)

    def create_node(self, node: Node):
        node.uuid = uuid.uuid4()
        node.init_widget()
        node.build()
        self.node_scene.addItem(node)
        pos = self.view.mapFromGlobal(QtGui.QCursor.pos())
        node.setPos(self.view.mapToScene(pos))

    def load_scene(self, json_path, imports):
        """ Load the scene from the json file """

        with open(json_path) as f:
            data = json.load(f)

        # clear out the python_node_interface lookup
        self.node_lookup = {}

        if data:

            # Add the nodes
            for n in data["nodes"]:
                info = imports[n["type"]]
                node = info["class"]()
                node.uuid = n["uuid"]
                node.value = n["value"]
                node.build()
                self.node_scene.addItem(node)
                node.setPos(n["x"], n["y"])
                self.node_lookup[node.uuid] = node

            # Add the connections
            for c in data["connections"]:
                start_pin = self.node_lookup[c["start_uuid"]].get_pin(c["start_pin"])
                end_pin = self.node_lookup[c["end_uuid"]].get_pin(c["end_pin"])

                connection = Connection(None)
                self.node_scene.addItem(connection)

                if start_pin:
                    connection.set_start_pin(start_pin)
                if end_pin:
                    connection.set_end_pin(end_pin)

                connection.update_start_and_end_pos()

    def save_project(self, json_path):
        """ Save the scene to the json file """

        scene = {"nodes": [], "connections": []}

        for item in self.node_scene.items():

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

                scene["nodes"].append(node)

            # Connections
            if isinstance(item, Connection):

                connection = {
                    "start_uuid": str(item.start_pin.node.uuid),
                    "end_uuid": str(item.end_pin.node.uuid),
                    "start_pin": item.start_pin.name,
                    "end_pin":  item.end_pin.name,
                }

                scene["connections"].append(connection)
                continue

            # Pins
            if isinstance(item, Pin):
                # Future code
                continue

        with open(json_path, "w") as f:
            json.dump(scene, f, indent=4)
