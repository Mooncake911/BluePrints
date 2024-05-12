from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor

from .layouts import PortLayout, MassageLayout, TopicLayout, MenuLayout


class ConsoleInput(QWidget):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

        self.layout = QVBoxLayout()

        self.menu_layout = MenuLayout(self.reload)
        self.port_layout = PortLayout(self.text_edit)
        self.topic_layout = TopicLayout(self.text_edit)
        self.message_layout = MassageLayout(self.text_edit, self.port_layout.serialPort)

        self.layout.addLayout(self.menu_layout)
        self.layout.addLayout(self.port_layout)
        self.layout.addLayout(self.topic_layout)
        self.layout.addLayout(self.message_layout)

        self.setLayout(self.layout)

    def reload(self):
        self.port_layout.newSession()
        self.message_layout.newSession()
        self.topic_layout.newSession()

        self.text_edit.clear()
        self.text_edit.setTextColor(QColor(255, 255, 255))
        self.text_edit.append(f"~ --- New session --- ~")
