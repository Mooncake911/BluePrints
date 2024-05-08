from PySide6.QtWidgets import QTabWidget, QTabBar

from info_widgets import NodeInfo
from node_editor import NodeEditor
from protocol_client import ProtocolClient

from node_editor.gui.attributes import Node


class Windows(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

        # Create node editor
        self.node_editor = NodeEditor(self.descriptionTab)
        self.addTab(self.node_editor, "Node Editor")
        self.tabBar().setTabButton(self.indexOf(self.node_editor), QTabBar.ButtonPosition.RightSide, None)

        # Create console window
        self.protocol_client = ProtocolClient()
        self.addTab(self.protocol_client, "Logger")
        self.tabBar().setTabButton(self.indexOf(self.protocol_client), QTabBar.ButtonPosition.RightSide, None)

    def descriptionTab(self, item):
        if isinstance(item, Node):
            node_info = NodeInfo(item.description)
            self.addTab(node_info, f"{item.name} Info")
            self.setCurrentWidget(node_info)
        else:
            print(f"{item} is not a node")

    def closeTab(self, index):
        self.removeTab(index)

    def closeEvent(self, event):
        self.node_editor.closeEvent(event)
        self.protocol_client.closeEvent(event)
        super().closeEvent(event)
