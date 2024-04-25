from PySide6.QtWidgets import QSplitter
from PySide6.QtGui import Qt

from .gui import InputLogWidget, OutputLogWidget


class Logger(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        self.output_widget = OutputLogWidget()
        self.input_widget = InputLogWidget(self.output_widget.logger)

        self.addWidget(self.input_widget)
        self.addWidget(self.output_widget)
