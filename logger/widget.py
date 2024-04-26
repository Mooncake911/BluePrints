from PySide6.QtWidgets import QSplitter
from PySide6.QtGui import Qt

from .gui import InputLogWidget, Console


class Logger(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        self.console = Console()
        self.input_log = InputLogWidget(self.console.logger)

        self.addWidget(self.input_log)
        self.addWidget(self.console)
