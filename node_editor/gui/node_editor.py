from contextlib import suppress

from PySide6 import QtCore

from ..connection import Connection
from ..node import Node
from ..pin import Pin


class NodeEditor(QtCore.QObject):
    """ Constructor for NodeEditor. """
    def __init__(self, parent):
        super().__init__(parent)
        self.connection = None
        self.port = None
        self.scene = None
        self._last_selected = None

    def install(self, scene):
        """ Installs the NodeEditor into a QGraphicsScene. """
        self.scene = scene
        self.scene.installEventFilter(self)

    def item_at(self, position):
        """ Returns the QGraphicsItem at the given position. """
        items = self.scene.items(QtCore.QRectF(position - QtCore.QPointF(1, 1), QtCore.QSizeF(3, 3)))
        return items[0] if items else None

    def eventFilter(self, watched, event):
        """ Filters events from the QGraphicsScene."""
        if event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.port = self.item_at(event.scenePos())

                if isinstance(self.port, Pin):
                    self.connection = Connection(None)
                    self.scene.addItem(self.connection)
                    self.connection.start_pos = self.port.scenePos()
                    self.connection.end_pos = self.port.scenePos()
                    self.connection.update_path()
                    return True

                if self._last_selected:
                    # If we clear the scene, we loose the last selection
                    with suppress(RuntimeError):
                        self._last_selected.select_connections(False)

                if isinstance(self.port, Node):
                    self.port.select_connections(True)
                    self._last_selected = self.port

                else:
                    self._last_selected = None

            elif event.button() == QtCore.Qt.MouseButton.RightButton:
                # context menu
                pass

        # Process finished with exit code -1073741819 (0xC0000005)
        # Описание: все Nodes которые содержат в себе QtWidgets.QWidget() при 3-х разовом удалении
        elif event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Delete:
                for item in self.scene.selectedItems():
                    item.delete()

            if event.key() == QtCore.Qt.Key.Key_A:
                node_items = [item for item in self.scene.items() if isinstance(item, Node)]
                all_selected = len(self.scene.selectedItems()) == len(node_items)
                for item in node_items:
                    item.setSelected(not all_selected)

            return True

        elif event.type() == QtCore.QEvent.Type.GraphicsSceneMouseMove:
            if self.connection:
                self.connection.end_pos = event.scenePos()
                self.connection.update_path()
                return True

        elif event.type() == QtCore.QEvent.Type.GraphicsSceneMouseRelease:
            # TODO the conditions bellow don't let multi-connection
            if self.connection and event.button() == QtCore.Qt.MouseButton.LeftButton:
                item = self.item_at(event.scenePos())

                if isinstance(item, Pin):
                    if self.port.can_connect_to(item):

                        if item.connection:
                            item.connection.delete()

                        if self.port.connection:
                            self.port.connection.delete()

                        if self.port.connection == item.connection:
                            self.port.clear_connection()
                            item.clear_connection()

                        self.connection.set_start_pin(self.port)
                        self.connection.set_end_pin(item)
                        self.connection.update_start_and_end_pos()

                    else:
                        self.connection.delete()

                    self.connection = None

                # connection to nowhere
                if self.connection:
                    self.connection.delete()

                self.connection = None
                self.port = None
                return True

        return super().eventFilter(watched, event)
