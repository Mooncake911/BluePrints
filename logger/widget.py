from PySide6.QtWidgets import QSplitter
from PySide6.QtGui import Qt

from .gui import ConsoleInput, Console


class Logger(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        self.console = Console()
        self.input = ConsoleInput(self.console.text_edit)

        self.addWidget(self.input)
        self.addWidget(self.console)
