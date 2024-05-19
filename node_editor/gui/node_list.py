from PySide6 import QtCore, QtGui, QtWidgets

from db.redis_db import redis_manager
from node_editor.example import NODES_LIST, Device_Node

NODE_IMPORTS = {}


class NodeList(QtWidgets.QTreeWidget):
    root_path = 'root'

    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)
        self.setDragEnabled(True)

        self.load_nodes()
        self.update_project()

    @staticmethod
    def load_nodes():
        for parent, nodes in NODES_LIST.items():
            for node in nodes:
                NODE_IMPORTS[node.__name__] = {"parent": parent, "class": node}

    @staticmethod
    def load_devices():
        devices_names = list(redis_manager.keys())
        NODE_IMPORTS.update({name: {"parent": "Device Nodes", "class": Device_Node}
                             for name in devices_names})

    def find_item_by_text(self, name):
        # Searching for an item by name in the tree
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.name == name:
                return item
        # Create, if it's absent
        item = QtWidgets.QTreeWidgetItem([name])
        item.name = name
        item.parent_name = self.root_path
        item.class_name = None
        return item

    def update_project(self):
        self.clear()
        self.load_devices()

        for name, data in NODE_IMPORTS.items():

            if data["parent"] == self.root_path:
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
