from PySide6 import QtCore, QtGui, QtWidgets

from .attributes import Node
from .node_connection import NodeConnection

from node_editor.gui.utils import Utils


class ViewScene(QtWidgets.QGraphicsScene):
    def __init__(self, description_tab_func):
        super().__init__()
        self.description_tab_func = description_tab_func
        self.setSceneRect(0, 0, 9999, 9999)

        # Set the node connection event filter
        self.node_connection = NodeConnection(self)
        self.installEventFilter(self.node_connection)

        self.utils = Utils(self)

    def dragMoveEvent(self, event):
        """
        This method is called when a drag and drop event enters the view.
        It checks if the mime data format is "text/plain" and accepts or ignores the event accordingly.
        """
        event.acceptProposedAction()
        event.accept()

    def dropEvent(self, event):
        """
        This method is called when a drag and drop event is dropped onto the view.
        It retrieves the name of the dropped node from the mime data and emits a signal to request the creation of the
        corresponding node.
        """
        mime_data = event.mimeData()
        item = mime_data.item

        if item.name and item.class_name:
            node = item.class_name(name=item.name)
            node.setPos(event.scenePos())
            node.init_widget()
            self.addItem(node)
        return super().dropEvent(event)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.scenePos(), QtGui.QTransform())

        if item:
            if isinstance(item, Node):
                menu = QtWidgets.QMenu()

                info_action = QtGui.QAction("ℹ️ Info")
                info_action.triggered.connect(lambda: self.description_tab_func(item))
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
                self.utils.extra_message()

            # [Ctrl + C]
            if event.key() == QtCore.Qt.Key.Key_C:
                pass

            # [Ctrl + V]
            if event.key() == QtCore.Qt.Key.Key_V:
                pass

        return super().keyPressEvent(event)
