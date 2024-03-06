from PySide6 import QtWidgets
from PySide6.QtGui import QDoubleValidator

from node_editor.node import Node


class Float_Node(Node):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()

        self.title_text = "Float"
        self.type_text = "Data Types"
        self.set_color(title_color=(75, 0, 130))

        self.add_pin(name="Value", is_output=True)

    def init_widget(self):
        line_edit = QtWidgets.QLineEdit()

        # Устанавливаем валидатор для ограничения ввода только целых чисел
        double_validator = QDoubleValidator()
        line_edit.setValidator(double_validator)
        double_validator.setDecimals(5)

        # Устанавливаем текст по умолчанию
        line_edit.setPlaceholderText("Enter")

        # Устанавливаем геометрию
        self.widget.setFixedWidth(100)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(line_edit)
        self.widget.setLayout(layout)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)

        super().init_widget()
