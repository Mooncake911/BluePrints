from PySide6 import QtCore, QtGui, QtWidgets

from node_editor.attributes import Node
from node_editor.utils import extra_message

from .node_connection import NodeConnection
from .node_list import DEVICE_NODES


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
        if name in DEVICE_NODES:
            # Device Nodes from database
            node = class_name(
                name=name,
                pins={"is_output": [], "is_input": ["brightness", "mode"]}
            )
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
        # TODO contex menu for Nodes
        item = self.itemAt(event.scenePos(), QtGui.QTransform())

        if item:
            if isinstance(item, Node):
                menu = QtWidgets.QMenu()
                hello_action = QtGui.QAction("Contex menu", self)
                menu.addAction(hello_action)
                action = menu.exec_(event.screenPos())

                if action == hello_action:
                    print("Hello")

        return super().contextMenuEvent(event)

    def keyPressEvent(self, event):
        """
        This method is called when happened any press key event.
        It checks the key's relevant shortcuts.
        """
        # Delete selected elements
        if event.key() == QtCore.Qt.Key.Key_Delete:
            for item in self.selectedItems():
                item.delete()

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            node_items = [item for item in self.items() if isinstance(item, Node)]

            # [Ctrl + A]
            if event.key() == QtCore.Qt.Key.Key_A:
                all_selected = len(self.selectedItems()) == len(node_items)
                for item in node_items:
                    item.setSelected(not all_selected)

            # [Ctrl + N]
            if event.key() == QtCore.Qt.Key.Key_N:
                extra_message(self)

        return super().keyPressEvent(event)
