from PySide6 import QtWidgets

from node_editor.node import Node


class Timer_Node(Node):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()

        self.title_text = "Timer"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 165, 0))

        self.add_pin(name="::Ex In", is_output=False, execution=True)
        self.add_pin(name="::Ex Out", is_output=True, execution=True)

    def init_widget(self):
        self.widget.setFixedWidth(100)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        tmr = QtWidgets.QTimeEdit()
        tmr.setDisplayFormat("hh:mm:ss")
        layout.addWidget(tmr)
        self.widget.setLayout(layout)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)

        super().init_widget()
