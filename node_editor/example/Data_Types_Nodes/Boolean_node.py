from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Boolean_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_text = "Boolean"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 69, 0))

        self.add_pin(pin_text="Value", is_output=True, pin_type="bool")

    def user_input(self, text):
        self.metadata["value"] = bool(text)

    def init_widget(self):
        value = self.metadata.get("value", 0)

        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(["False", "True"])
        combo_box.setCurrentIndex(value)
        combo_box.currentIndexChanged.connect(self.user_input)
        combo_box.setFixedWidth(100)

        self.layout.addWidget(combo_box)

        super().init_widget()
