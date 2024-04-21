from PySide6 import QtCore


from .attributes import Connection, Pin


class NodeConnection(QtCore.QObject):
    """ Constructor for NodeEditor. """
    def __init__(self, scene):
        super().__init__()
        self.connection = None
        self.from_pin = None
        self.to_pin = None
        self.scene = scene

    def item_at(self, position):
        """ Returns the QGraphicsItem at the given position. """
        items = self.scene.items(QtCore.QRectF(position - QtCore.QPointF(1, 1), QtCore.QSizeF(3, 3)))
        return items[0] if items else None

    def eventFilter(self, watched, event):
        """ Filters events from the QGraphicsScene."""
        if event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.from_pin = self.item_at(event.scenePos())

                if isinstance(self.from_pin, Pin):
                    self.connection = Connection()
                    self.connection.start_pos = self.from_pin.scenePos()
                    self.connection.end_pos = self.from_pin.scenePos()
                    self.scene.addItem(self.connection)
                    return True

        elif event.type() == QtCore.QEvent.Type.GraphicsSceneMouseMove:
            if self.connection:
                self.connection.end_pos = event.scenePos()
                self.connection.update_path()
                return True

        elif event.type() == QtCore.QEvent.Type.GraphicsSceneMouseRelease:
            # TODO the conditions bellow don't let multi-connection
            if self.connection and event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.to_pin = self.item_at(event.scenePos())

                if isinstance(self.to_pin, Pin):
                    if self.from_pin.can_connect_to(self.to_pin):

                        if self.to_pin.connection:
                            self.to_pin.connection.delete()

                        if self.from_pin.connection:
                            self.from_pin.connection.delete()

                        if self.from_pin.connection == self.to_pin.connection:
                            self.from_pin.clear_connection()
                            self.to_pin.clear_connection()

                        self.connection.set_start_pin(self.from_pin)
                        self.connection.set_end_pin(self.to_pin)
                        self.connection.update_start_and_end_pos()

                    else:
                        self.connection.delete()

                else:
                    # connection to nowhere
                    if self.connection:
                        self.connection.delete()

                self.connection = None
                self.from_pin = None
                self.to_pin = None
                return True

        return super().eventFilter(watched, event)
