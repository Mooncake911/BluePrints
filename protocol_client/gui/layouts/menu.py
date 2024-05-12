from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QStyle)


class MenuLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 30
    _layout_space = 20

    def __init__(self, button_func):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.label = QLabel()
        self.label.setText("Reload:")
        self.label.setFixedWidth(self._label_width)

        self.button = QPushButton()
        self.button.setFixedSize(self._button_width, self._button_width)
        icon = self.button.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.button.setIcon(icon)
        self.button.setIconSize(self.button.size())
        self.button.clicked.connect(button_func)
        self.button.clicked.connect(self.execute)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.addWidget(self.label)
        self.addWidget(self.button)
        self.addItem(self.spacer)

    def execute(self):
        """ Анимация нажатия кнопки перезагрузки """
        pass
