from pathlib import Path
import importlib.util
import inspect

from PySide6 import QtCore, QtGui, QtWidgets


class NodeList(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        except Exception as e:
            print(f"Error loading module {file}: {e}")

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
