from PySide6 import QtWidgets, QtGui
from node_editor.gui.attributes import Node


class String_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_edit = QtWidgets.QLineEdit()

        self.title_text = "String"
        self.type_text = "Data Types"
        self.set_color(title_color=(0, 128, 0))

        self.add_pin(pin_text="Value", is_output=True, pin_type="str")

    def line_edit_user_input(self, value):
        self.metadata["value"] = value

    def init_widget(self):
        # Line Edit
        value = self.metadata.get("value")
        self.line_edit_user_input(value)
        if value:
            self.line_edit.setText(value)
        else:
            self.line_edit.setPlaceholderText("Enter")
        self.line_edit.textChanged.connect(self.line_edit_user_input)
        self.line_edit.setFixedWidth(100)
        self.layout.addWidget(self.line_edit)

        super().init_widget()
