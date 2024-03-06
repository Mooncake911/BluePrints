from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets

from ..node import Node


class View(QtWidgets.QGraphicsView):
    """
    View class for python_node_interface editor.
    """

    _background_color = QtGui.QColor(38, 38, 38)

    _grid_pen_s = QtGui.QPen(QtGui.QColor(52, 52, 52, 255), 0.5)
    _grid_pen_l = QtGui.QPen(QtGui.QColor(22, 22, 22, 255), 1.0)

    _grid_size_fine = 15
    _grid_size_course = 150

    _mouse_wheel_zoom_rate = 0.0015

    request_node = QtCore.Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._manipulationMode = 0

        gl_format = QtGui.QSurfaceFormat()
        gl_format.setSamples(10)
        QtGui.QSurfaceFormat.setDefaultFormat(gl_format)
        gl_widget = QtOpenGLWidgets.QOpenGLWidget()

        self.currentScale = 1
        self._pan = False
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._numScheduledScaling = 0
        self.lastMousePos = QtCore.QPoint()

        self.setViewport(gl_widget)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def wheelEvent(self, event):
        """
        Handles the wheel events, e.g. zoom in/out.
        :param event: Wheel event.
        """
        # sometimes you can trigger the wheel when panning, so we disable when panning
        if self._pan:
            return

        num_degrees = event.angleDelta() / 8.0
        num_steps = num_degrees.y() / 5.0
        self._numScheduledScaling += num_steps

        # If the user moved the wheel another direction, we reset previously scheduled scaling
        if self._numScheduledScaling * num_steps < 0:
            self._numScheduledScaling = num_steps

        self.anim = QtCore.QTimeLine()
        self.anim.setUpdateInterval(20)
        self.anim.valueChanged.connect(self.scaling_time)
        self.anim.finished.connect(self.anim_finished)
        self.anim.start()

    def scaling_time(self, x):
        """
        Updates the current scale based on the wheel events.
        :param x: The value of the current time.
        """
        factor = 1.0 + self._numScheduledScaling / 300.0
        self.currentScale *= factor

        if self.currentScale > 1.2:
            self.currentScale = 1.2
        elif self.currentScale < 0.1:
            self.currentScale = 0.1
        else:
            self.scale(factor, factor)

    def anim_finished(self):
        """
        Called when the zoom animation is finished.
        """
        if self._numScheduledScaling > 0:
            self._numScheduledScaling -= 1
        else:
            self._numScheduledScaling += 1

    def drawBackground(self, painter, rect):
        """
        Draws the background for the python_node_interface editor view.

        :param painter: The painter to draw with.
        :param rect: The rectangle to be drawn.
        """

        def fill_grid(grid_size, grid_pen):
            left = int(rect.left()) - (int(rect.left()) % grid_size)
            top = int(rect.top()) - (int(rect.top()) % grid_size)

            # Draw horizontal lines
            grid_lines = []
            painter.setPen(grid_pen)
            y = float(top)
            while y < float(rect.bottom()):
                grid_lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
                y += grid_size
            painter.drawLines(grid_lines)

            # Draw vertical lines
            grid_lines = []
            painter.setPen(grid_pen)
            x = float(left)
            while x < float(rect.right()):
                grid_lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
                x += grid_size
            painter.drawLines(grid_lines)

        painter.fillRect(rect, self._background_color)
        fill_grid(self._grid_size_fine, self._grid_pen_s)  # fine squares
        fill_grid(self._grid_size_course, self._grid_pen_l)  # course squares

        return super().drawBackground(painter, rect)

    def contextMenuEvent(self, event):
        """
        This method is called when a context menu event is triggered in the view. It finds the item at the event
        position and shows a context menu if the item is a Node.
        """
        cursor = QtGui.QCursor()
        # origin = self.mapFromGlobal(cursor.pos())
        pos = self.mapFromGlobal(cursor.pos())
        item = self.itemAt(event.pos())

        if item:
            if isinstance(item, Node):
                print("Found Node", item)

                menu = QtWidgets.QMenu(self)

                hello_action = QtGui.QAction("Hello", self)

                menu.addAction(hello_action)
                action = menu.exec_(self.mapToGlobal(pos))

                if action == hello_action:
                    print("Hello")

    def dragEnterEvent(self, e):
        """
        This method is called when a drag and drop event enters the view. It checks if the mime data format is
        "text/plain" and accepts or ignores the event accordingly.
        """
        if e.mimeData().hasFormat("text/plain"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        This method is called when a drag and drop event is dropped onto the view. It retrieves the name of the dropped
        python_node_interface from the mime data and emits a signal to request the creation of the corresponding
        python_node_interface.
        """
        node = e.mimeData().item.class_name
        if node:
            self.request_node.emit(node())

    def mousePressEvent(self, event):
        """
        This method is called when a mouse press event occurs in the view. It sets the cursor to a closed hand cursor
        and enables panning if the middle mouse button is pressed.
        """
        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            self._pan = True
            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        This method is called when a mouse release event occurs in the view. It sets the cursor back to the arrow cursor
        and disables panning if the middle mouse button is released.
        """
        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            self._pan = False
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        This method is called when a mouse move event occurs in the view. It pans the view if the middle mouse button is
        pressed and moves the mouse.
        """
        if self._pan:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self._pan_start_x))

            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self._pan_start_y))

            self._pan_start_x = event.x()
            self._pan_start_y = event.y()

        return super().mouseMoveEvent(event)
