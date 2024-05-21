import time
import json

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy)

from .gui import NodeList, View, ViewScene
from .func import test2

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
        id_list = [1, 2]
        requests = [json.dumps({"type": "request", "message": {"id": i}}) for i in id_list]
        for message in requests:
            serial_port.put(message)
            time.sleep(2)

#        time.sleep(2)

        self.node_list.update_project()

    def execute(self):
        scene_data = self.view_scene.utils.save_scene()
        data = test2(scene_data)
        serial_port.put(data)

    def closeEvent(self, event):
        if serial_port.is_open:
            serial_port.close()
