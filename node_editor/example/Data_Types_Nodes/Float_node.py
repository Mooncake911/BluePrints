from PySide6 import QtWidgets, QtGui
from node_editor.gui.attributes import Node


class Float_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_text = "Float"
        self.type_text = "Data Types"
        self.set_color(title_color=(75, 0, 130))

        self.add_pin(pin_text="Value", is_output=True, pin_type="float")

    def user_input(self, text):
        self.metadata["value"] = float(text)

    def init_widget(self):
        # Set float validator
        validator = QtGui.QDoubleValidator()
        validator.setDecimals(5)

        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.user_input)
        line_edit.setValidator(validator)
        line_edit.setFixedWidth(100)

        value = str(self.metadata.get("value"))
        if value:
            line_edit.setText(value)
        else:
            line_edit.setPlaceholderText("Enter")

        self.layout.addWidget(line_edit)

        super().init_widget()
