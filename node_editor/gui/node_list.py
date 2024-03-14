import json
from pathlib import Path
import importlib.util
import inspect

from PySide6 import QtCore, QtGui, QtWidgets

from node_editor.attributes import Node, Connection, Pin


class NodeList(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setDragEnabled(True)

        self.nodes_path = Path('node_editor/example')
        self.imports = {}

        for f in self.nodes_path.rglob("*.py"):
            self.load_module(f)

        self.update_project()

    def load_module(self, file):
        try:
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if not name.endswith('_Node'):
                    continue
                if inspect.isclass(obj):
                    # print(file.parts[1:-1])
                    self.imports[obj.__name__] = {"parent": file.parent.name, "class": obj, "module": module}
        except ModuleNotFoundError as e:
            print(e)

    def find_item_by_text(self, text):
        # Поиск элемента по тексту в дереве
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.text(0) == text:
                return item
        # Если его нет, то создаём
        item = QtWidgets.QTreeWidgetItem([text])
        item.module = None
        item.class_name = None
        return item

    def update_project(self):
        temp_list = []

        for name, data in self.imports.items():
            name = name.replace("_Node", "")
            parent_name = data["parent"].replace("_", " ")
            parent_item = None

            if parent_name == self.nodes_path.stem:
                item = QtWidgets.QTreeWidgetItem([name])
                temp_list.append(item)
            else:
                parent_item = self.find_item_by_text(parent_name)
                item = QtWidgets.QTreeWidgetItem(parent_item, [name])
                parent_item.addChild(item)

            item.module = data["module"]
            item.class_name = data["class"]

            if parent_item:
                self.addTopLevelItem(parent_item)

        for item in temp_list:
            self.addTopLevelItem(item)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.text(0):  # Используем text(0) для получения текста из первой колонки
            name = item.text(0)

            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            mime_data.setText(name)
            mime_data.item = item
            drag.setMimeData(mime_data)

            # Drag needs a pixmap or else it'll error due to a null pixmap
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor("darkgray"))
            drag.setPixmap(pixmap)
            drag.exec_()

            super().mousePressEvent(event)

    def load_scene(self, scene, json_path):
        """ Load the scene from the json file """

        with open(json_path) as f:
            data = json.load(f)

        if data:
            node_lookup = {}  # A dictionary of nodes, by uuids

            # Add the nodes
            for n in data["nodes"]:
                if n["type"] in self.imports.keys():
                    info = self.imports[n["type"]]
                    node = info["class"]()
                    node.uuid = n["uuid"]
                    node.value = n["value"]
                    pos = QtCore.QPointF(n["x"], n["y"])

                    scene.create_node(node, pos)

                    node_lookup[node.uuid] = node

                else:
                    print(f"{n['type']} module is not found.")
                    return

            # Add the connections
            for c in data["connections"]:
                if node_lookup:
                    start_pin = node_lookup[c["start_uuid"]].get_pin(c["start_pin"])
                    end_pin = node_lookup[c["end_uuid"]].get_pin(c["end_pin"])

                    connection = Connection()
                    scene.addItem(connection)

                    if start_pin:
                        connection.set_start_pin(start_pin)
                    if end_pin:
                        connection.set_end_pin(end_pin)

                    connection.update_start_and_end_pos()

    @staticmethod
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
                    "end_pin": item.end_pin.name,
                }

                json_scene["connections"].append(connection)

            # Pins
            if isinstance(item, Pin):
                # Future code
                continue

        with open(json_path, "w") as f:
            json.dump(json_scene, f, indent=4)
