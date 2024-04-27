from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Boolean_Node(Node):
    def __init__(self, name, scene):
        super().__init__(name, scene)

        self.title_text = "Boolean"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 69, 0))

        self.add_pin(pin_text="Value", is_output=True, pin_type="bool")

    def user_input(self, text):
        self.value = text

    def init_widget(self):
        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(["False", "True"])
        combo_box.currentIndexChanged.connect(self.user_input)
        combo_box.setFixedWidth(100)

        if self.value:
            combo_box.setCurrentIndex(self.value)

        self.layout.addWidget(combo_box)

        super().init_widget()
