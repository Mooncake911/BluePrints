from PySide6.QtWidgets import QSplitter, QTextEdit
from PySide6.QtGui import Qt

from .gui import ConsoleInput, Console


class ProtocolClient(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        self.text_edit = QTextEdit()  # common item
        self.console = Console(text_edit=self.text_edit)
        self.console_input = ConsoleInput(text_edit=self.text_edit)

        self.addWidget(self.console_input)
        self.addWidget(self.console)

    def closeEvent(self, event):
        self.console_input.closeEvent(event)
        self.console.closeEvent(event)
        super().closeEvent(event)
