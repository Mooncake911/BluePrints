from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTextEdit)
from PySide6.QtGui import QFont


class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.logger = QTextEdit()
        self.logger.setFont(QFont("Arial", 10))
        self.logger.setReadOnly(True)
        self.logger.setPlaceholderText('Log Message')
        self.layout.addWidget(self.logger)

        self.button = QPushButton('Clear')
        self.button.clicked.connect(self.logger.clear)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
