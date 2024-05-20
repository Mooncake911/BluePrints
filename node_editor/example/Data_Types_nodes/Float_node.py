from PySide6 import QtWidgets, QtGui
from node_editor.gui.attributes import Node


class Float_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_edit = QtWidgets.QLineEdit()

        self.title_text = "Float"
        self.type_text = "Data Types"
        self.set_color(title_color=(75, 0, 130))

        self.add_pin(pin_text="Value", is_output=True, pin_type="float")

    def line_edit_user_input(self, value):
        if value == '-':
            pass
        else:
            self.metadata["value"] = float(value) if value else 0.0

    def init_widget(self):
        # Set float validator
        validator = QtGui.QDoubleValidator()
        validator.setDecimals(5)
        self.line_edit.setValidator(validator)

        # Line Edit
        value = self.metadata.get("value", 0.0)
        self.line_edit_user_input(value)
        if value:
            self.line_edit.setText(str(value))
        else:
            self.line_edit.setPlaceholderText(str(value))
        self.line_edit.textChanged.connect(self.line_edit_user_input)
        self.line_edit.setFixedWidth(100)
        self.layout.addWidget(self.line_edit)

        super().init_widget()
