from PySide6 import QtWidgets
from node_editor.attributes import Node


class Event_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Event"
        self.type_text = "Event Nodes"
        self.set_color(title_color=(128, 0, 0))

        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)
        self.add_pin(pin_text="value", is_output=True)

    def button_cmd(self):
        print("btn command")
        # self.execute()

    def init_widget(self):
        button = QtWidgets.QPushButton("Button test")
        button.clicked.connect(self.button_cmd)
        button.setFixedWidth(100)
        self.layout.addWidget(button)

        super().init_widget()
