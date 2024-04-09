from PySide6 import QtCore, QtGui, QtWidgets


class ConnectionGraphics(QtWidgets.QGraphicsPathItem):
    def __init__(self):
        super().__init__()

        self.setFlag(QtWidgets.QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(-1)

        self.start_pos = QtCore.QPointF()
        self.end_pos = QtCore.QPointF()
        self.start_pin = None
        self.end_pin = None

        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def hoverEnterEvent(self, event):
        self.setSelected(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setSelected(False)
        super().hoverLeaveEvent(event)

    def update_path(self):
        """
        Draws a smooth cubic curve from the start to end pins.
        """
        path = QtGui.QPainterPath()
        path.moveTo(self.start_pos)

        dx = self.end_pos.x() - self.start_pos.x()
        dy = self.end_pos.y() - self.start_pos.y()

        ctr1 = QtCore.QPointF(self.start_pos.x() + dx * 0.5, self.start_pos.y())
        ctr2 = QtCore.QPointF(self.start_pos.x() + dx * 0.5, self.start_pos.y() + dy)
        path.cubicTo(ctr1, ctr2, self.end_pos)

        self.setPath(path)

    def paint(self, painter, option=None, widget=None):
        """
        Override the default paint method depending on if the object is selected.
        """
        # Get a palette from any of the scene views
        palette = self.scene().views()[0].palette()
        base_color = palette.color(QtGui.QPalette.ColorRole.Base)

        thickness = 4
        color = QtGui.QColor(255 - base_color.red(), 255 - base_color.green(), 255 - base_color.blue(), 200)

        if self.start_pin:
            if self.start_pin.execution:
                thickness = 6  # Change thickness for execution pin
            else:
                color = QtGui.QColor(0, 128, 255, 200)  # Change color for non-execution pin

        if self.isSelected():
            painter.setPen(QtGui.QPen(color.lighter(), thickness + 4))
        else:
            painter.setPen(QtGui.QPen(color, thickness))

        painter.drawPath(self.path())
