from PySide6.QtWidgets import QSplitter
from PySide6.QtGui import Qt

from .gui import ConsoleInput, Console


class ProtocolClient(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        self.console = Console()
        self.console_input = ConsoleInput(text_edit=self.console.text_edit)

        self.addWidget(self.console_input)
        self.addWidget(self.console)
