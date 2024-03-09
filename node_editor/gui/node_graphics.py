from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from ..common import NodeStatus


class NodeGraphics(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.widget = QtWidgets.QWidget()
        self.widget.resize(0, 0)

        self.size = QtCore.QRectF()  # Size of Node
        self.status = NodeStatus.CLEAN  # Status of Node
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

        self.title_bg_height = 35  # background title height
        self.horizontal_margin = 15  # horizontal margin
        self.vertical_margin = 15  # vertical margin

    def get_status_color(self):
        if self.status == NodeStatus.CLEAN:
            return QtGui.QColor(0, 100, 0)
        elif self.status == NodeStatus.DIRTY:
            return QtGui.QColor(255, 165, 0)
        elif self.status == NodeStatus.ERROR:
            return QtGui.QColor(139, 0, 0)

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
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QtGui.QPen(self.title_bg_color.lighter(), 2))
            painter.drawPath(self.main_bg_path.simplified())

    def build(self):
        """ Builds the node interface by constructing its graphical representation. """

        # Configure the widget side of things.
        self.widget.setStyleSheet("background-color: " + self.main_bg_color.name() + ";")

        # Node width and height
        total_width = self.widget.width()
        total_height = self.title_bg_height + self.widget.height()

        # The fonts what will be used
        title_font = QtGui.QFont("Lucida Sans Unicode", pointSize=12)
        type_font = QtGui.QFont("Lucida Sans Unicode", pointSize=8)
        pin_font = QtGui.QFont("Lucida Sans Unicode")

        # Get the dimensions of the title and type
        title_dim = {
            "w": QtGui.QFontMetrics(title_font).horizontalAdvance(self.title_text),
            "h": QtGui.QFontMetrics(title_font).height(),
        }

        type_dim = {
            "w": QtGui.QFontMetrics(type_font).horizontalAdvance(self.type_text),
            "h": QtGui.QFontMetrics(type_font).height(),
        }

        # Get the max width
        total_width = max(title_dim["w"], type_dim["w"], total_width)

        pin_dim = None
        # Add the height for each of the pins
        for pin in self._pins:
            pin_dim = {
                "w": QtGui.QFontMetrics(pin_font).horizontalAdvance(pin.name),
                "h": QtGui.QFontMetrics(pin_font).height(),
            }
            total_height += pin_dim["h"]

        # Add the margin to the total_width
        total_width += self.horizontal_margin
        total_height += self.vertical_margin

        self.size = QtCore.QRectF(-total_width / 2, -total_height / 2, total_width, total_height)

        # Draw the background rectangle
        self.main_bg_path.setFillRule(Qt.WindingFill)
        self.main_bg_path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, total_height, 5, 5)

        # Draw the title rectangle
        self.title_bg_path.setFillRule(Qt.WindingFill)
        self.title_bg_path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, self.title_bg_height, 2, 2)

        # Draw the status rectangle
        self.status_path.setFillRule(Qt.WindingFill)
        self.status_path.addRoundedRect(total_width / 2 - 12, -total_height / 2 + 2, 10, 10, 2, 2)

        # Draw the title
        self.title_path.addText(
            -total_width / 2 + 5,
            (-total_height / 2) + title_dim["h"] / 2 + 5,
            title_font,
            self.title_text,
        )

        # Draw the type
        self.type_path.addText(
            -total_width / 2 + 5,
            (-total_height / 2) + title_dim["h"] + 5,
            type_font,
            self.type_text,
        )

        # Position the pins. Execution pins stay on the same row
        if pin_dim:
            y = self.title_bg_height - total_height / 2 - 10

            # Do the execution pins
            for pin in self._pins:
                y += pin_dim["h"]

                if pin.is_output:
                    pin.setPos(total_width / 2 - 10, y)
                else:
                    pin.setPos(-total_width / 2 + 10, y)

        # move the widget to the bottom
        self.widget.move(int(-self.widget.width() / 2), int(total_height / 2 - self.widget.height() - 10))
