from pathlib import Path
import importlib.util
import inspect

from PySide6 import QtCore, QtGui, QtWidgets


from node_editor.example.Device_Nodes.Device_node import Device_Node
from devices import DEVICES_NAMES

NODE_IMPORTS = {}


class NodeList(QtWidgets.QTreeWidget):
    nodes_path = Path('node_editor/example')

    def __init__(self):
        super().__init__()

        global NODE_IMPORTS

        self.setHeaderHidden(True)
        self.setDragEnabled(True)

        for f in self.nodes_path.rglob("*.py"):
            self.load_module(f)

        self.update_project()

    @staticmethod
    def load_module(file):
        try:
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and name != 'Node':  # ignore parent Node class from node.py
                    if file.parent.name == "Device_Nodes":
                        NODE_IMPORTS.update({i: {"parent": file.parent.name, "class": Device_Node}
                                             for i in DEVICES_NAMES.keys()})
                    else:
                        # print(spec.name, obj.__name__)
                        NODE_IMPORTS[obj.__name__] = {"parent": file.parent.name, "class": obj}

        except ModuleNotFoundError as e:
            print(e)

    def find_item_by_text(self, name):
        # Searching for an item by name in the tree
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.name == name:
                return item
        # Create, if it's absent
        item = QtWidgets.QTreeWidgetItem([name])
        item.name = name
        item.parent_name = self.nodes_path.name
        item.class_name = None
        return item

    def update_project(self):
        for name, data in NODE_IMPORTS.items():

            if data["parent"] == self.nodes_path.name:
                item = QtWidgets.QTreeWidgetItem([name])
                self.addTopLevelItem(item)

            else:
                parent_item = self.find_item_by_text(data["parent"])
                item = QtWidgets.QTreeWidgetItem(parent_item, [name])
                parent_item.addChild(item)
                self.addTopLevelItem(parent_item)

            item.name = name
            item.parent_name = data["parent"]  # parent_name is a custom variable
            item.class_name = data["class"]  # class_name is a custom variable

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())

        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.item = item
        drag.setMimeData(mime_data)

        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(QtGui.QColor("darkgray"))

        drag.setPixmap(pixmap)
        drag.exec_()

        super().mousePressEvent(event)
