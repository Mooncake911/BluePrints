from PySide6 import QtWidgets, QtGui
from node_editor.attributes import Node


class Integer_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Integer"
        self.type_text = "Data Types"
        self.set_color(title_color=(0, 255, 255))

        self.add_pin(pin_text="Value", is_output=True)

    def user_input(self, text):
        self.value = text

    def init_widget(self):
        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.user_input)
        line_edit.setFixedWidth(100)

        # Set integer validator
        int_validator = QtGui.QIntValidator()
        line_edit.setValidator(int_validator)
        int_validator.setRange(-2147483647, 2147483647)

        # Set default text
        if self.value:
            line_edit.setText(self.value)
        else:
            line_edit.setPlaceholderText("Enter")

        self.inner_widget = line_edit

        super().init_widget()
