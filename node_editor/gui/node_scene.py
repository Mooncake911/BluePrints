from PySide6 import QtGui, QtWidgets
from ..node import Node


class NodeScene(QtWidgets.QGraphicsScene):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos(), QtGui.QTransform())
        if item.setAcceptDrops:
            # pass on event to item at the coordinates
            item.dropEvent(e)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

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
