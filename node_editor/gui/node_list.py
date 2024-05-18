from pathlib import Path
import importlib.util
import inspect

from PySide6 import QtCore, QtGui, QtWidgets


from db.redis_db import redis_manager
from node_editor.example.Device_Nodes.Device_node import Device_Node


NODE_IMPORTS = {}


class NodeList(QtWidgets.QTreeWidget):
    nodes_path = Path('node_editor/example')

    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)
        self.setDragEnabled(True)

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
                                             for i in redis_manager.keys()})
                    else:
                        # print(spec.name, obj.__name__)
                        NODE_IMPORTS[obj.__name__] = {"parent": file.parent.name, "class": obj}

            # write_node_imports(NODE_IMPORTS) don't necessary because it's list

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
        self.clear()

        for file in self.nodes_path.rglob("*.py"):
            self.load_module(file)

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

        mime_data = QtCore.QMimeData()
        mime_data.item = item
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)

        if item and item.class_name is not None:
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor("darkgray"))
        else:
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor("red"))

        drag.setPixmap(pixmap)
        drag.exec()

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.mousePressEvent(event)
        super().mouseDoubleClickEvent(event)

    def expandAllItems(self):
        for item in self.findItems("", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive):
            item.setExpanded(True)

    def collapseAllItems(self):
        for item in self.findItems("", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive):
            item.setExpanded(False)

    def keyPressEvent(self, event):
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.key() == QtCore.Qt.Key.Key_Down:
                self.expandAllItems()
            elif event.key() == QtCore.Qt.Key.Key_Up:
                self.collapseAllItems()
        else:
            super().keyPressEvent(event)
