from PySide6 import QtCore, QtGui, QtWidgets


class PinGraphics(QtWidgets.QGraphicsPathItem):
    _radius = 5
    _margin = 3

    def __init__(self, parent, pin_text: str, is_output: bool, execution: bool, visible: bool = True):
        super().__init__(parent)

        self.connection = None
        self.node = parent
        self.pin_text = pin_text
        self.is_output = is_output
        self.execution = execution
        self.visible = visible

        self.icon_pin_path = QtGui.QPainterPath()
        self.title_pin_path = QtGui.QPainterPath()

        self.pin_font = QtGui.QFont("Lucida Sans Unicode", pointSize=8)
        self.pin_dim = {
            "w": QtGui.QFontMetrics(self.pin_font).horizontalAdvance(self.pin_text),
            "h": QtGui.QFontMetrics(self.pin_font).height(),
        }

        self.setFlag(QtWidgets.QGraphicsPathItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def paint_pin_icon(self, painter):
        if bool(self.connection):
            if self.execution:
                painter.setPen(QtCore.Qt.GlobalColor.white)
                painter.setBrush(QtCore.Qt.GlobalColor.white)
            else:
                painter.setPen(QtCore.Qt.GlobalColor.green)
                painter.setBrush(QtCore.Qt.GlobalColor.green)
        else:
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        self.setPath(self.icon_pin_path)
        painter.drawPath(self.icon_pin_path)

    def paint_pin_title(self, painter):
        if self.visible:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(QtCore.Qt.GlobalColor.white)
        else:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(self.title_pin_path)

    def paint(self, painter, option=None, widget=None):
        self.paint_pin_icon(painter)
        self.paint_pin_title(painter)

    def build(self):
        # Build icon
        if self.execution:
            # Draw arrow (connection)
            points = [QtCore.QPointF(-6, -7), QtCore.QPointF(-6, 7), QtCore.QPointF(-2, 7), QtCore.QPointF(6, 0),
                      QtCore.QPointF(-2, -7), QtCore.QPointF(-6, -7)]
            self.icon_pin_path.setFillRule(QtCore.Qt.FillRule.WindingFill)
            self.icon_pin_path.addPolygon(QtGui.QPolygonF(points))
        else:
            # Draw circle (connection)
            self.icon_pin_path.setFillRule(QtCore.Qt.FillRule.WindingFill)
            self.icon_pin_path.addEllipse(-self._radius, -self._radius, 2 * self._radius, 2 * self._radius)

        # Build tittle
        icon_pin_size = self._radius + self._margin
        if self.is_output:
            x = -icon_pin_size - self.pin_dim["w"]
        else:
            x = icon_pin_size
        y = self.pin_dim["h"] / 4
        self.title_pin_path.addText(x, y, self.pin_font, self.pin_text)

    def itemChange(self, change, value):
        if self.connection:
            self.connection.update_start_and_end_pos()
        return super().itemChange(change, value)
