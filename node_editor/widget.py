from PySide6.QtWidgets import (QSplitter, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QSpacerItem, QSizePolicy)
from PySide6.QtGui import Qt

from .gui import NodeList, View, ViewScene
from .func import test, get_config


class MenuLayout(QHBoxLayout):
    _layout_space = 18

    def __init__(self, view_scene: ViewScene, node_list: NodeList, view: View, serialPort):
        super().__init__()
        self.setSpacing(self._layout_space)
        self.setContentsMargins(7, 7, 7, 0)

        self.view_scene = view_scene
        self.node_list = node_list
        self.view = view
        self.serialPort = serialPort

        self.button1 = QPushButton("Fast search")
        self.button1.clicked.connect(self.fast_search)
        self.addWidget(self.button1)

        self.button2 = QPushButton("Deep search")
        self.button2.clicked.connect(self.fast_search)
        self.addWidget(self.button2)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.addItem(self.spacer)

        self.button3 = QPushButton("Execute")
        self.button3.clicked.connect(self.execute)
        self.addWidget(self.button3)

    def fast_search(self):
        for message in get_config([1]):
            self.serialPort.write(message)

        import time
        time.sleep(2)

        self.node_list.update_project()

    def execute(self):
        scene_data = self.view_scene.utils.save_scene()
        test(scene_data)


class NodeEditor(QWidget):
    def __init__(self, description_tab_func, serialPort):
        super().__init__()
        self.description_tab_func = description_tab_func
        self.serialPort = serialPort

        # Create scene
        self.view_scene = ViewScene(self.description_tab_func)
        # Create left widget
        self.node_list = NodeList()
        # Create right widget
        self.view = View(self.view_scene)

        # Create menu
        self.menu = MenuLayout(self.view_scene, self.node_list, self.view, self.serialPort)

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
        super().closeEvent(event)

