import uuid

from PySide6 import QtWidgets

from .pin import Pin
from .node_graphics import NodeGraphics


class Node(NodeGraphics):
    uuid_list = []

    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get("name")  # A name of widget from NodeList
        self.metadata = kwargs.get("metadata", dict())
        self.description = "description"

        self.uuid = uuid.uuid4()  # An identifier that used to manage nodes (ex. saving and loading scene)
        while self.uuid in self.uuid_list:
            self.uuid = uuid.uuid4()
        self.uuid_list.append(self.uuid)

        self.proxy = QtWidgets.QGraphicsProxyWidget()
        self.proxy.setParentItem(self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)

    def init_widget(self):
        self.proxy.setWidget(self.widget)
        self.build()

    def delete(self):
        for pin in self._pins:
            pin.clear_connection()

        self.scene().removeItem(self.proxy)
        self.scene().removeItem(self)

    def get_start_pin(self, name):
        for pin in self._pins:
            if pin.is_output and pin.name == name:
                return pin

    def get_end_pin(self, name):
        for pin in self._pins:
            if not pin.is_output and pin.name == name:
                return pin

    def add_pin(self, pin_text: str = "PIN NAME", pin_type: str = "",
                is_output: bool = False, execution: bool = False, visible: bool = True):
        pin = Pin(self, name=pin_text, pin_type=pin_type, is_output=is_output, execution=execution, visible=visible)
        self._pins.append(pin)
