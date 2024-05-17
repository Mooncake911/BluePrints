from PySide6.QtWidgets import (QSplitter, QFileDialog, QWidget, QVBoxLayout)
from PySide6.QtGui import Qt

from .gui import NodeList, View, ViewScene
from .menu import MenuLayout


class NodeEditor(QWidget):
    def __init__(self, description_tab_func):
        super().__init__()
        self.description_tab_func = description_tab_func

        # Create scene
        self.view_scene = ViewScene(self.description_tab_func)
        # Create left widget
        self.node_list = NodeList()
        # Create right widget
        self.view = View(self.view_scene)

        # Create menu
        self.menu = MenuLayout(self.view_scene, self.node_list, self.view)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addLayout(self.menu)
        layout.addWidget(self.splitter())
        # layout.setContentsMargins(7, 7, 7, 7)
        self.setLayout(layout)

    def splitter(self):
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(self.node_list)
        splitter.addWidget(self.view)
        splitter.setContentsMargins(7, 7, 7, 7)
        return splitter

    def save_project(self):
        self.view_scene.utils.file_message(mode=QFileDialog.AcceptMode.AcceptSave)

    def load_project(self):
        self.view_scene.utils.file_message(mode=QFileDialog.AcceptMode.AcceptOpen)

    def closeEvent(self, event):
        if self.view_scene.items():
            self.view_scene.utils.extra_message()
        self.menu.closeEvent(event)
        super().closeEvent(event)
