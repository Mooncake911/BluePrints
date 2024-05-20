from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Boolean_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.combo_box = QtWidgets.QComboBox()

        self.title_text = "Boolean"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 69, 0))

        self.add_pin(pin_text="Value", is_output=True, pin_type="bool")

    def combo_box_user_input(self, value):
        self.metadata["value"] = bool(value)

    def init_widget(self):

        # Combo Box
        value = self.metadata.get("value", 0)
        self.combo_box_user_input(value)
        self.combo_box.addItems(["False", "True"])
        self.combo_box.setCurrentIndex(value)
        self.combo_box.currentIndexChanged.connect(self.combo_box_user_input)
        self.combo_box.setFixedWidth(100)
        self.layout.addWidget(self.combo_box)

        super().init_widget()
