from PySide6 import QtWidgets, QtGui
from node_editor.gui.attributes import Node


class Float_Node(Node):
    def __init__(self, name, scene):
        super().__init__(name, scene)

        self.title_text = "Float"
        self.type_text = "Data Types"
        self.set_color(title_color=(75, 0, 130))

        self.add_pin(pin_text="Value", is_output=True, pin_type="float")

    def user_input(self, text):
        self.value = text

    def init_widget(self):
        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.user_input)
        line_edit.setFixedWidth(100)

        # Set float validator
        double_validator = QtGui.QDoubleValidator()
        line_edit.setValidator(double_validator)
        double_validator.setDecimals(5)

        # Set default text
        if self.value:
            line_edit.setText(self.value)
        else:
            line_edit.setPlaceholderText("Enter")

        self.layout.addWidget(line_edit)

        super().init_widget()
