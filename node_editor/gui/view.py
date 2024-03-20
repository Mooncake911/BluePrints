from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets
from .node_editor import NodeEditor


class View(QtWidgets.QGraphicsView):
    _scaler = 1.1

    _grid_pen_s = QtGui.QPen(QtGui.QColor(52, 52, 52, 255), 0.5)
    _grid_pen_l = QtGui.QPen(QtGui.QColor(22, 22, 22, 255), 1.0)

    _grid_size_fine = 15
    _grid_size_course = 150

    def _zoom(self, delta):
        factor = self._scaler if delta > 0 else 1 / self._scaler
        if (0.1 < self.transform().m11() * factor < 2) and (0.1 < self.transform().m22() * factor < 2):
            # print(self.transform().m11(), self.transform().m22())
            self.scale(factor, factor)

    def _change_place(self, event, button):
        if event.button() in button:
            self._pan = True
            self._start_pos = event.pos()
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        self._pan = False
        self._start_pos = QtCore.QRectF()

        # Set node editor
        self.node_editor = NodeEditor()

        # Graphic settings
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        gl_format = QtGui.QSurfaceFormat()
        gl_format.setSamples(10)
        QtGui.QSurfaceFormat.setDefaultFormat(gl_format)
        gl_widget = QtOpenGLWidgets.QOpenGLWidget()
        self.setViewport(gl_widget)

        # Location settings
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Set Buttons
        # self.zoom_in_button = QtWidgets.QPushButton("+")
        # self.zoom_out_button = QtWidgets.QPushButton("-")
        # self.zoom_in_button.clicked.connect(lambda: self._zoom(1))
        # self.zoom_out_button.clicked.connect(lambda: self._zoom(-1))
        #
        # layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(self.zoom_in_button)
        # layout.addWidget(self.zoom_out_button)
        # layout.setContentsMargins(10, 10, 10, 10)
        # self.setLayout(layout)

        # Other add settings of View
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def setScene(self, scene):
        self.node_editor.setScene(scene)
        super().setScene(scene)

    def drawBackground(self, painter, rect):
        """
        Draws the background for the interface editor view. [draw in live: because of zoom in/out]

        :param painter: The painter to draw with.
        :param rect: The rectangle to be drawn.
        """

        def fill_grid(grid_size, grid_pen):
            y = float(int(rect.left()) - (int(rect.left()) % grid_size))
            x = float(int(rect.top()) - (int(rect.top()) % grid_size))

            grid_lines = []
            painter.setPen(grid_pen)

            # Draw horizontal lines
            while x < float(rect.bottom()):
                grid_lines.append(QtCore.QLineF(rect.left(), x, rect.right(), x))
                x += grid_size
            painter.drawLines(grid_lines)

            # Draw vertical lines
            while y < float(rect.right()):
                grid_lines.append(QtCore.QLineF(y, rect.top(), y, rect.bottom()))
                y += grid_size
            painter.drawLines(grid_lines)

        painter.fillRect(rect, self.palette().color(QtGui.QPalette.ColorRole.Base))
        fill_grid(self._grid_size_fine, self._grid_pen_s)  # fine squares
        fill_grid(self._grid_size_course, self._grid_pen_l)  # course squares

        return super().drawBackground(painter, rect)

    # ------------------------------------------ View Events ----------------------------------------------------------#
    def enterEvent(self, event):
        self.setFocus()
        super().enterEvent(event)

    def wheelEvent(self, event):
        """
        Handles the wheel events, e.g. zoom in/out.
        """
        # Sometimes you can trigger the wheel when panning, so we disable when panning
        if self._pan:
            return

        delta = event.angleDelta().y()
        self._zoom(delta)

        return super().wheelEvent(event)

    def keyPressEvent(self, event):
        """
        Handles the key press events, e.g. zoom in/out.
        """
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.key() == QtCore.Qt.Key.Key_Minus or event.key() == QtCore.Qt.Key.Key_Underscore:
                self._zoom(-1)
            if event.key() == QtCore.Qt.Key.Key_Plus or event.key() == QtCore.Qt.Key.Key_Equal:
                self._zoom(1)
        return super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """
        This method is called when a mouse press event occurs in the view.
        It sets the cursor to a closed hand cursor and enables panning if the middle mouse button is pressed.
        """
        self._change_place(event, button=QtCore.Qt.MouseButton.MiddleButton)
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
        This method is called when a double mouse press event occurs in the view.
        It sets the cursor to a closed hand cursor and enables panning if the left mouse button is pressed.
        """
        self._change_place(event, button=QtCore.Qt.MouseButton.LeftButton)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        This method is called when a mouse release event occurs in the view.
        It sets the cursor back to the arrow cursor and disables panning if the middle mouse button is released.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton or event.button() == QtCore.Qt.MouseButton.MiddleButton:
            self._pan = False
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        This method is called when a mouse move event occurs in the view.
        It pans the view if the middle mouse button is pressed and moves the mouse.
        """
        if self._pan:
            delta = event.pos() - self._start_pos
            self._start_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

        return super().mouseMoveEvent(event)
