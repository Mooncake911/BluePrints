from PySide6 import QtWidgets
from PySide6.QtGui import QIntValidator

from node_editor.attributes import Node


class Integer_Node(Node):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()

        self.title_text = "Integer"
        self.type_text = "Data Types"
        self.set_color(title_color=(0, 255, 255))

        self.add_pin(name="Value", is_output=True)

    def user_input(self, text):
        # print("User input:", text)
        self.value = text

    def init_widget(self):
        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.user_input)

        # Устанавливаем валидатор для ограничения ввода только целых чисел
        int_validator = QIntValidator()
        line_edit.setValidator(int_validator)
        int_validator.setRange(-2147483647, 2147483647)

        # Устанавливаем текст по умолчанию
        if self.value is not None:
            line_edit.setText(self.value)
        else:
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
