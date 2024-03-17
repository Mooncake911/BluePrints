import uuid

from PySide6 import QtWidgets


from .pin import Pin
from .node_graphics import NodeGraphics


class Node(NodeGraphics):
    def __init__(self):
        super().__init__()
        self.uuid = uuid.uuid4()  # An identifier that used to manage nodes (ex. saving and loading scene)
        self.value = None         # An input value that has been set by the user
        self.inner_widget = None

    def init_widget(self):
        # TODO мне не нравиться надо переделать
        if self.inner_widget:

            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.inner_widget)
            self.widget.setLayout(layout)

            proxy = QtWidgets.QGraphicsProxyWidget()
            proxy.setWidget(self.widget)
            proxy.setParentItem(self)

    def compute(self):
        raise NotImplementedError("compute is not implemented")

    def execute(self):
        # Get the values from the input pins
        self.execute_inputs()

        # Compute the value
        self.compute()

        # execute nodes connected to output
        self.execute_outputs()

    def execute_inputs(self):
        pass

    def execute_outputs(self):
        pass

    def delete(self):
        """
        Deletes the connection.

        This function removes any connected pins by calling :any:`Port.remove_connection` for each pin
        connected to this connection. After all connections have been removed, the stored :any:`Port`
        references are set to None. Finally, :any:`QGraphicsScene.removeItem` is called on the scene to
        remove this widget.

        Returns:
            None
        """

        to_delete = [pin.connection for pin in self._pins if pin.connection]
        for connection in to_delete:
            connection.delete()

        self.scene().removeItem(self)

    def get_pin(self, name):
        for pin in self._pins:
            if pin.name == name:
                return pin

    def add_pin(self, name, is_output, execution=False, visible=True):
        pin = Pin(self, name=name, is_output=is_output, execution=execution, visible=visible)
        self._pins.append(pin)

    def select_connections(self, selected: bool):
        """
        Sets the highlighting of all connected pins to the specified value.
        """

        for pin in self._pins:
            if pin.connection:
                pin.connection._do_highlight = selected
