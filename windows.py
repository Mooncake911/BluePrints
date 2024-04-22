from PySide6.QtWidgets import QTabWidget

from node_editor import NodeEditor
from logger import Logger


class Windows(QTabWidget):
    def __init__(self):
        super().__init__()

        # Create node editor
        self.node_editor = NodeEditor()
        self.addTab(self.node_editor, "Node Editor")

        # Create information window
        self.logger = Logger()
        self.addTab(self.logger, "Logger")

    def closeEvent(self, event):
        self.node_editor.closeEvent(event)
        super().closeEvent(event)
