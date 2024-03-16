from PySide6 import QtCore, QtGui, QtWidgets


class ConnectionGraphics(QtWidgets.QGraphicsPathItem):
    def __init__(self):
        super().__init__()

        self.setFlag(QtWidgets.QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)

        self.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 2))
        self.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        self.setZValue(-1)

        self.start_pos = QtCore.QPointF()
        self.end_pos = QtCore.QPointF()
        self.start_pin = None
        self.end_pin = None

        self._do_highlight = False

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
        Override the Adefault paint method depending on if the object is selected.
        """
        thickness = 4
        color = QtGui.QColor(0, 128, 255, 200)
        
        if self.start_pin:
            if self.start_pin.execution:
                thickness = 6
                color = QtGui.QColor(255, 255, 255, 150)

        if self.isSelected() or self._do_highlight:
            painter.setPen(QtGui.QPen(color.lighter(), thickness + 4))
        else:
            painter.setPen(QtGui.QPen(color, thickness))

        painter.drawPath(self.path())
