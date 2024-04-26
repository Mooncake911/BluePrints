import uuid

from PySide6 import QtWidgets

from .pin import Pin
from .node_graphics import NodeGraphics


class Node(NodeGraphics):
    def __init__(self, name=__name__, scene=None):
        super().__init__()

        self.scene = scene  # Global node editor scene
        self.name = name  # A name of widget from NodeList
        self.uuid = uuid.uuid4()  # An identifier that used to manage nodes (ex. saving and loading scene)
        self.value = None  # An input value that has been set by the user
        self.index = None  # An index that has been set by the user

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

        self.scene.removeItem(self.proxy)
        self.scene.removeItem(self)

    def get_start_pin(self, name):
        for pin in self._pins:
            if pin.is_output and pin.name == name:
                return pin

    def get_end_pin(self, name):
        for pin in self._pins:
            if not pin.is_output and pin.name == name:
                return pin

    def add_pin(self, pin_text: str = "PIN NAME", is_output: bool = False, execution: bool = False, visible: bool = True):
        pin = Pin(self, name=pin_text, is_output=is_output, execution=execution, visible=visible)
        self._pins.append(pin)

    @staticmethod
    def get_description():
        print("description")
