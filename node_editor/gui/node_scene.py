from PySide6 import QtCore, QtGui, QtWidgets
from ..node import Node


class NodeScene(QtWidgets.QGraphicsScene):
    request_node = QtCore.Signal(object)

    def dragEnterEvent(self, e):
        pass
        # e.acceptProposedAction()

    def dragMoveEvent(self, event):
        """
        This method is called when a drag and drop event enters the view. It checks if the mime data format is
        "text/plain" and accepts or ignores the event accordingly.
        """
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        This method is called when a drag and drop event is dropped onto the view.
        It retrieves the name of the dropped node from the mime data and emits a signal to request the creation of the
        corresponding node.
        """
        node = event.mimeData().item.class_name
        if node:
            self.request_node.emit(node())

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
