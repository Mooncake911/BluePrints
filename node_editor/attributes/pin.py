from PySide6 import QtCore, QtGui, QtWidgets


class Pin(QtWidgets.QGraphicsPathItem):
    _radius = 5
    _margin = 2

    def __init__(self, parent, node, name, is_output, execution, visible=True):
        super().__init__(parent)

        self.setFlag(QtWidgets.QGraphicsPathItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

        self.node = node
        self.name = name
        self.is_output = is_output
        self.execution = execution
        self.visible = visible
        self.connection = None

    def clear_connection(self):
        if self.connection:
            self.connection.delete()

    def can_connect_to(self, pin):
        if not pin:
            return False
        if pin.node == self.node:
            return False
        return self.is_output != pin.is_output and pin.execution == self.execution

    def is_connected(self):
        return bool(self.connection)

    def set_pin(self, painter):
        path = QtGui.QPainterPath()
        if self.execution:
            # Determine arrow (connection)
            points = [QtCore.QPointF(-6, -7), QtCore.QPointF(-6, 7), QtCore.QPointF(-2, 7), QtCore.QPointF(6, 0),
                      QtCore.QPointF(-2, -7), QtCore.QPointF(-6, -7)]
            path.addPolygon(QtGui.QPolygonF(points))
            painter.setPen(QtCore.Qt.GlobalColor.white)
        else:
            # Determine circle (connection)
            path.addEllipse(-self._radius, -self._radius, 2 * self._radius, 2 * self._radius)
            painter.setPen(QtCore.Qt.GlobalColor.green)
        self.setPath(path)

        if self.is_connected():
            if self.execution:
                painter.setBrush(QtCore.Qt.GlobalColor.white)
            else:
                painter.setBrush(QtCore.Qt.GlobalColor.green)
        else:
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def set_pin_name(self, painter):
        path = QtGui.QPainterPath()

        font = QtGui.QFont()
        font_metrics = QtGui.QFontMetrics(font)
        pin_text_height = font_metrics.height()
        pin_text_width = font_metrics.horizontalAdvance(self.name)

        if self.is_output:
            x = -self._radius - self._margin - pin_text_width
        else:
            x = self._radius + self._margin

        y = pin_text_height / 4

        path.addText(x, y, font, self.name)

        if self.visible:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(QtCore.Qt.GlobalColor.white)
            painter.drawPath(path)

    def paint(self, painter, option=None, widget=None):
        # Define pin:
        self.set_pin(painter)
        self.set_pin_name(painter)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemScenePositionHasChanged and self.connection:
            self.connection.update_start_and_end_pos()
        return value
