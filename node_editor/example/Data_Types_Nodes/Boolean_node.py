from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Boolean_Node(Node):
    def __init__(self, name):
        super().__init__(name)

        self.title_text = "Boolean"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 69, 0))

        self.add_pin(pin_text="Value", is_output=True)

    def init_widget(self):
        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(["True", "False"])
        combo_box.setFixedWidth(100)
        self.layout.addWidget(combo_box)

        super().init_widget()
