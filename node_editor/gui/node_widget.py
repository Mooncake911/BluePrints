import json
import uuid

from PySide6 import QtGui, QtWidgets

from .node_editor import NodeEditor
from .view import View

from ..connection import Connection
from ..node import Node
from ..pin import Pin


class NodeScene(QtWidgets.QGraphicsScene):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos(), QtGui.QTransform())
        if item.setAcceptDrops:
            # pass on event to item at the coordinates
            item.dropEvent(e)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()


class NodeWidget(QtWidgets.QWidget):
    """
    Widget for creating and displaying a python_node_interface editor.

    Attributes:
        node_editor (NodeEditor): The python_node_interface editor object.
        scene (NodeScene): The scene object for the python_node_interface editor.
        view (View): The view object for the python_node_interface editor.
    """

    def __init__(self, parent):
        """
        Initializes the NodeWidget object.

        Args:
            parent (QWidget): The parent widget.
        """
        super().__init__(parent)

        self.node_lookup = {}  # A dictionary of nodes, by uuids for faster looking up. Refactor this in the future
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.node_editor = NodeEditor(self)
        self.scene = NodeScene()
        self.scene.setSceneRect(0, 0, 9999, 9999)
        self.view = View(self)
        self.view.setScene(self.scene)
        self.node_editor.install(self.scene)

        main_layout.addWidget(self.view)

        self.view.request_node.connect(self.create_node)

    def create_node(self, node: Node):
        node.uuid = uuid.uuid4()
        node.build()
        self.scene.addItem(node)
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
                self.scene.addItem(node)
                node.setPos(n["x"], n["y"])
                self.node_lookup[node.uuid] = node

            # Add the connections
            for c in data["connections"]:
                start_pin = self.node_lookup[c["start_uuid"]].get_pin(c["start_pin"])
                end_pin = self.node_lookup[c["end_uuid"]].get_pin(c["end_pin"])

                connection = Connection(None)
                self.scene.addItem(connection)

                if start_pin:
                    connection.set_start_pin(start_pin)
                if end_pin:
                    connection.set_end_pin(end_pin)

                connection.update_start_and_end_pos()

    def save_project(self, json_path):
        """ Save the scene to the json file """

        scene = {"nodes": [], "connections": []}

        for item in self.scene.items():

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
