from PySide6.QtWidgets import QSplitter, QFileDialog
from PySide6.QtGui import Qt

from .gui import NodeList, View, ViewScene


class NodeEditor(QSplitter):
    def __init__(self, description_tab_func):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)

        # Create scene
        self.scene = ViewScene(description_tab_func)
        # Create left widget
        self.node_list = NodeList()
        # Create right widget
        self.view = View(self.scene)

        self.addWidget(self.node_list)
        self.addWidget(self.view)
        self.setContentsMargins(7, 7, 7, 7)

    def save_project(self):
        self.scene.utils.file_message(mode=QFileDialog.AcceptMode.AcceptSave)

    def load_project(self):
        self.scene.utils.file_message(mode=QFileDialog.AcceptMode.AcceptOpen)

    def closeEvent(self, event):
        if self.scene.items():
            self.scene.utils.extra_message()
        super().closeEvent(event)
