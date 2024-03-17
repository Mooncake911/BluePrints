from pathlib import Path
import importlib.util
import inspect

from PySide6 import QtCore, QtGui, QtWidgets


GLOBAL_IMPORTS = {}


class NodeList(QtWidgets.QTreeWidget):
    nodes_path = Path('node_editor/example')

    def __init__(self):
        super().__init__()

        global GLOBAL_IMPORTS

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
                if inspect.isclass(obj) and name.endswith('_Node'):
                    # print(file.parts[1:-1])
                    GLOBAL_IMPORTS[obj.__name__] = {"parent": file.parent.name, "class": obj, "module": module}

        except ModuleNotFoundError as e:
            print(e)

    def find_item_by_text(self, text):
        # Searching for an item by text in the tree
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.text(0) == text:
                return item
        # Create, if it's absent
        item = QtWidgets.QTreeWidgetItem([text])
        item.module = None
        item.class_name = None
        return item

    def update_project(self):
        temp_list = []

        for name, data in GLOBAL_IMPORTS.items():
            name = name.replace("_Node", "")
            parent_name = data["parent"].replace("_", " ")
            parent_item = None

            if parent_name == data["parent"]:
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
        if item and item.text(0):
            name = item.text(0)

            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            mime_data.setText(name)
            mime_data.item = item
            drag.setMimeData(mime_data)

            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor("darkgray"))

            drag.setPixmap(pixmap)
            drag.exec_()

        super().mousePressEvent(event)
