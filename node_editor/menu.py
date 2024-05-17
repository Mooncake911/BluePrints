from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy)

from .gui import NodeList, View, ViewScene
from .func import test, get_config

from serial_port import serial_port


class MenuLayout(QHBoxLayout):
    _layout_space = 18

    def __init__(self, view_scene: ViewScene, node_list: NodeList, view: View):
        super().__init__()
        self.setSpacing(self._layout_space)
        self.setContentsMargins(7, 7, 7, 0)

        self.view_scene = view_scene
        self.node_list = node_list
        self.view = view

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
            serial_port.put(message)

        import time
        time.sleep(2)

        self.node_list.update_project()

    def execute(self):
        scene_data = self.view_scene.utils.save_scene()
        test(scene_data)

    def closeEvent(self, event):
        if serial_port.is_open:
            serial_port.close()