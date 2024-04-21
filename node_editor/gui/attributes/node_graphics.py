from PySide6 import QtCore, QtGui, QtWidgets

from .status import NodeStatus


class NodeGraphics(QtWidgets.QGraphicsItem):

    _title_bg_height = 35  # background title height
    _horizontal_margin = 15  # horizontal margin
    _vertical_margin = 10  # vertical margin

    def __init__(self):
        super().__init__()

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # Initialize widget (skeleton)
        self.widget = QtWidgets.QWidget()
        self.widget.resize(0, 0)

        self.size = QtCore.QRectF()  # Size of Node
        self.status = NodeStatus.ERROR  # Status of Node
        self._pins = []  # A list of pins

        self.title_text = "Title"
        self.type_text = "Type"

        self.main_bg_color = QtGui.QColor(25, 25, 25, 200)  # background
        self.title_bg_color = QtGui.QColor(255, 0, 0)  # background

        self.main_bg_path = QtGui.QPainterPath()  # The main Node background path
        self.title_bg_path = QtGui.QPainterPath()  # The title background path
        self.title_path = QtGui.QPainterPath()  # The title path
        self.type_path = QtGui.QPainterPath()  # The type path
        self.status_path = QtGui.QPainterPath()  # The status path

        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def hoverEnterEvent(self, event):
        self.setSelected(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if event.modifiers() != QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setSelected(False)
        super().hoverLeaveEvent(event)

    def get_status_color(self):
        if all(pin.connection is None for pin in self._pins):
            self.status = NodeStatus.ERROR
            return QtGui.QColor(255, 0, 0)
        elif any(pin.connection is None for pin in self._pins):
            self.status = NodeStatus.WARNING
            return QtGui.QColor(255, 255, 0)
        else:
            self.status = NodeStatus.CLEAN
            return QtGui.QColor(0, 255, 0)

    def boundingRect(self):
        return self.size

    def set_color(self, title_color=(255, 0, 0), background_color=(25, 25, 25, 200)):
        self.title_bg_color = QtGui.QColor(*title_color)
        self.main_bg_color = QtGui.QColor(*background_color)

    def paint(self, painter, option=None, widget=None):
        """
        Paints the node interface on the given painter.

        Args:
            painter (QtGui.QPainter): The painter to use for drawing the node interface.
            option (QStyleOptionGraphicsItem): The style options to use for drawing the node interface (optional)
            widget (QWidget): The widget to use for drawing the node interface (optional).
        """

        # Main background of Node
        painter.setBrush(self.main_bg_color)
        painter.setPen(self.main_bg_color.lighter())
        painter.drawPath(self.main_bg_path.simplified())

        # Header background of Node
        gradient = QtGui.QLinearGradient()
        gradient.setStart(0, -90)
        gradient.setFinalStop(0, 0)
        gradient.setColorAt(0, self.title_bg_color.lighter())  # Start color (light)
        gradient.setColorAt(1, self.title_bg_color.darker())  # End color (dark)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(self.title_bg_color)
        painter.drawPath(self.title_bg_path.simplified())

        # Text in Header (title, type)
        painter.setBrush(QtCore.Qt.GlobalColor.white)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawPath(self.title_path)
        painter.drawPath(self.type_path)

        # Status in Header
        painter.setBrush(self.get_status_color().lighter())
        painter.setPen(self.get_status_color().darker())
        painter.drawPath(self.status_path.simplified())

        # The highlight around Main background
        if self.isSelected():
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.setPen(QtGui.QPen(self.title_bg_color.lighter(), 2))
            painter.drawPath(self.main_bg_path.simplified())

    def build(self):
        """
        Builds the node interface by constructing its graphical representation.
        """
        # Configure the widget side of things.
        # self.widget.setStyleSheet("background-color: " + self.main_bg_color.name() + ";")

        # Node width and height
        total_height = self.widget.height()
        total_width = self.widget.width()

        # The fonts what will be used
        title_font = QtGui.QFont("Lucida Sans Unicode", pointSize=12)
        type_font = QtGui.QFont("Lucida Sans Unicode", pointSize=8)

        # Get the dimensions of the title and type
        title_dim = {
            "w": QtGui.QFontMetrics(title_font).horizontalAdvance(self.title_text),
            "h": QtGui.QFontMetrics(title_font).height(),
        }

        type_dim = {
            "w": QtGui.QFontMetrics(type_font).horizontalAdvance(self.type_text),
            "h": QtGui.QFontMetrics(type_font).height(),
        }

        total_height += (title_dim["h"] + type_dim["h"])
        total_width = max(title_dim["w"], type_dim["w"], total_width)

        # Add the height for each of the pins
        for pin in self._pins:
            pin_dim = pin.pin_dim
            total_height += pin_dim["h"]
            total_width = max(pin_dim["w"], total_width)

        # Add the margin to the total_width
        total_width += self._horizontal_margin
        total_height += self._vertical_margin

        # The Node size
        self.size = QtCore.QRectF(-total_width / 2, -total_height / 2, total_width, total_height)

        # Draw the background rectangle
        self.main_bg_path.setFillRule(QtCore.Qt.FillRule.WindingFill)
        self.main_bg_path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, total_height, 5, 5)

        # Draw the title rectangle
        self.title_bg_path.setFillRule(QtCore.Qt.FillRule.WindingFill)
        self.title_bg_path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, self._title_bg_height, 2, 2)

        # Draw the status rectangle
        self.status_path.setFillRule(QtCore.Qt.FillRule.WindingFill)
        self.status_path.addRoundedRect(total_width / 2 - 12, -total_height / 2 + 2, 10, 10, 2, 2)

        # Draw the title
        self.title_path.addText(
            (-total_width + self._horizontal_margin) / 2,
            (-total_height + title_dim["h"] + self._vertical_margin) / 2,
            title_font,
            self.title_text,
        )

        # Draw the type
        self.type_path.addText(
            (-total_width + self._horizontal_margin) / 2,
            (-total_height + title_dim["h"] + title_dim["h"] + self._vertical_margin) / 2,
            type_font,
            self.type_text,
        )
        # Should be (-total_height + title_dim["h"] + type_dim["h"] + self._vertical_margin) / 2,
        # but we need an indent between tittle and type.

        # Draw the pins
        y = (-total_height + title_dim["h"] + title_dim["h"] + self._vertical_margin) / 2
        for pin in self._pins:
            y += pin.pin_dim["h"]
            if pin.is_output:
                pin.setPos(total_width / 2 - self._horizontal_margin, y)
            else:
                pin.setPos(-total_width / 2 + self._horizontal_margin, y)
            pin.build()

        # move the widget to the bottom
        self.widget.move(-self.widget.width() // 2, total_height // 2 - self.widget.height() - self._vertical_margin)
