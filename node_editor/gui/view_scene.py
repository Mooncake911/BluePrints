from PySide6 import QtCore, QtGui, QtWidgets

from node_editor.attributes import Node
from node_editor.utils import extra_message

from node_editor.devices import DEVICES_NAMES
from node_editor.example.Device_Nodes.Device_node import Device_Node

from .node_connection import NodeConnection


class ViewScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 9999, 9999)
        # Set the node connection editor
        self.node_connection = NodeConnection(self)
        self.installEventFilter(self.node_connection)

    def create_node(self, node, pos):
        node.init_widget()
        node.setPos(pos)
        self.addItem(node)

    @staticmethod
    def call_node_class(name, class_name):
        if class_name == Device_Node:
            # Device Nodes
            node = class_name(data=DEVICES_NAMES[name])
        else:
            # Default Nodes: Logic, Arithmetic, Data Types and etc.
            node = class_name()
        return node

    def dragMoveEvent(self, event):
        """
        This method is called when a drag and drop event enters the view.
        It checks if the mime data format is "text/plain" and accepts or ignores the event accordingly.
        """
        pass

    def dropEvent(self, event):
        """
        This method is called when a drag and drop event is dropped onto the view.
        It retrieves the name of the dropped node from the mime data and emits a signal to request the creation of the
        corresponding node.
        """
        mime_data = event.mimeData()
        item = mime_data.item
        pos = event.scenePos()

        if item.name and item.class_name:
            node = self.call_node_class(name=item.name, class_name=item.class_name)
            self.create_node(node, pos)
        return super().dropEvent(event)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.scenePos(), QtGui.QTransform())

        if item:
            if isinstance(item, Node):
                menu = QtWidgets.QMenu()

                info_action = QtGui.QAction("ℹ️ Info")
                info_action.triggered.connect(item.get_description)
                menu.addAction(info_action)

                delete_action = QtGui.QAction("❌ Delete")
                delete_action.triggered.connect(item.delete)
                menu.addAction(delete_action)

                menu.exec_(event.screenPos())

        return super().contextMenuEvent(event)

    def keyPressEvent(self, event):
        """
        This method is called when happened any press key event.
        It checks the key's relevant shortcuts.
        """
        # Delete selected elements [Del]
        if event.key() == QtCore.Qt.Key.Key_Delete:
            for item in self.selectedItems():
                item.delete()

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            node_items = [item for item in self.items() if isinstance(item, Node)]
            all_selected = len(self.selectedItems()) == len(node_items)

            # [Ctrl + A]
            if event.key() == QtCore.Qt.Key.Key_A:
                for item in node_items:
                    item.setSelected(not all_selected)

            # [Ctrl + N]
            if event.key() == QtCore.Qt.Key.Key_N:
                extra_message(self)

            # [Ctrl + C]
            if event.key() == QtCore.Qt.Key.Key_C:
                pass

            # [Ctrl + V]
            if event.key() == QtCore.Qt.Key.Key_V:
                pass

        return super().keyPressEvent(event)
