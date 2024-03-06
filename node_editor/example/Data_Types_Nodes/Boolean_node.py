from PySide6 import QtWidgets

from node_editor.node import Node


class Boolean_Node(Node):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()

        self.title_text = "Boolean"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 69, 0))

        self.add_pin(name="Value", is_output=True)

    def init_widget(self):
        self.widget.setFixedWidth(100)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        combo_box = QtWidgets.QComboBox()
        geek_list = ["True", "False"]
        combo_box.setGeometry(200, 150, 120, 30)
        combo_box.addItems(geek_list)
        layout.addWidget(combo_box)
        self.widget.setLayout(layout)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)

        super().init_widget()
