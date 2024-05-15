from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QLineEdit, QCompleter)
from PySide6.QtGui import Qt
from PySide6.QtCore import QStringListModel


class MassageLayout(QHBoxLayout):
    _history = ["dev1", "dev2"]

    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, logger, serial_port):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.logger = logger
        self.serialPort = serial_port

        self.label_text = "Message:"
        self.button_labels = ["Send"]

        self.label = QLabel()
        self.line_edit = QLineEdit()
        self.completer = QCompleter()
        self.button = QPushButton()

        self.initUI()

    def newSession(self):
        self.line_edit.clear()
        self.button.setText(self.button_labels[0])

    def initUI(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setModel(QStringListModel(self._history))

        self.line_edit.setCompleter(self.completer)

        self.button.setText(self.button_labels[0])
        self.button.setFixedWidth(self._button_width)
        self.button.clicked.connect(self.execute)

        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def execute(self):
        user_input = self.line_edit.text()

        # Remember user input
        if user_input not in self._history:
            self._history.append(user_input)
            self.completer.setModel(QStringListModel(self._history))

        self.messageRequest(user_input)

    def messageRequest(self, message: str) -> None:
        self.serialPort.write(message)
        self.serialPort.read()
