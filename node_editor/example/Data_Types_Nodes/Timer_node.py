from PySide6 import QtWidgets
from node_editor.attributes import Node


class Timer_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Timer"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 165, 0))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

    def init_widget(self):
        time_edit = QtWidgets.QTimeEdit()
        time_edit.setDisplayFormat("hh:mm:ss")
        time_edit.setFixedWidth(100)

        self.inner_widget = time_edit

        super().init_widget()
