from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor

from .layouts import PortLayout, MassageLayout, TopicLayout, MenuLayout


class ConsoleInput(QWidget):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.layout = QVBoxLayout()

        self.menu_layout = MenuLayout(self.execute)
        self.port_layout = PortLayout(self.logger)
        self.topic_layout = TopicLayout(self.logger)
        self.message_layout = MassageLayout(self.logger, self.port_layout.serialPort)
        self.execute()

        self.layout.addLayout(self.menu_layout)
        self.layout.addLayout(self.port_layout)
        self.layout.addLayout(self.topic_layout)
        self.layout.addLayout(self.message_layout)

        self.setLayout(self.layout)

    def execute(self):
        self.port_layout.newSession()
        self.message_layout.newSession()
        self.topic_layout.newSession()

        self.logger.clear()
        self.logger.setTextColor(QColor(255, 255, 255))
        self.logger.append(f"~ --- New session --- ~")
