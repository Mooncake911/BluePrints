from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton)
from PySide6.QtGui import QFont


class Console(QWidget):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

        self.layout = QVBoxLayout()

        self.text_edit.setFont(QFont("Arial", 10))
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText('Log Message')
        self.layout.addWidget(self.text_edit)

        self.button = QPushButton('Clear 🗑')
        self.button.clicked.connect(self.text_edit.clear)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        super().closeEvent(event)
