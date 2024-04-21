from PySide6.QtWidgets import QTabWidget

from node_editor import NodeEditor


class Windows(QTabWidget):
    def __init__(self):
        super().__init__()

        # Create node editor
        self.node_editor = NodeEditor()
        self.addTab(self.node_editor, "Node Editor")

    def closeEvent(self, event):
        self.node_editor.closeEvent(event)
        super().closeEvent(event)
