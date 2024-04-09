import json

from PySide6 import QtCore, QtGui, QtWidgets

from node_editor.attributes import Node, Connection
from node_editor.gui import GLOBAL_IMPORTS, DEVICE_NODES
from node_editor.utils import file_message, extra_message


class ViewScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 9999, 9999)

    def create_node(self, node, pos):
        self.addItem(node)
        node.init_widget()
        node.build()
        node.setPos(pos)

    @staticmethod
    def call_node_class(name, class_name):
        if name in DEVICE_NODES:
            # Device Nodes from database
            node = class_name(
                name=name,
                pins={"is_output": [], "is_input": ["brightness", "mode"]}
            )
        else:
            # Default Nodes: Logic, Arithmetic, Data Types and etc.
            node = class_name()
        return node

    def dragMoveEvent(self, event):
        """
        This method is called when a drag and drop event enters the view.
        It checks if the mime data format is "text/plain" and accepts or ignores the event accordingly.
        """
        pass

    def dropEvent(self, event):
        """
        This method is called when a drag and drop event is dropped onto the view.
        It retrieves the name of the dropped node from the mime data and emits a signal to request the creation of the
        corresponding node.
        """
        mime_data = event.mimeData()
        item = mime_data.item
        pos = event.scenePos()

        if item.name:
            node = self.call_node_class(name=item.name, class_name=item.class_name)
            self.create_node(node, pos)
        return super().dropEvent(event)

    def contextMenuEvent(self, event):
        # TODO contex menu for Nodes
        item = self.itemAt(event.scenePos(), QtGui.QTransform())

        if item:
            if isinstance(item, Node):
                menu = QtWidgets.QMenu()
                hello_action = QtGui.QAction("Contex menu", self)
                menu.addAction(hello_action)
                action = menu.exec_(event.screenPos())

                if action == hello_action:
                    print("Hello")

        return super().contextMenuEvent(event)

    def keyPressEvent(self, event):
        """
        This method is called when happened any press key event.
        It checks the key's relevant shortcuts.
        """
        # Delete selected elements
        if event.key() == QtCore.Qt.Key.Key_Delete:
            for item in self.selectedItems():
                item.delete()
            # TODO Process finished with exit code -1073741819 (0xC0000005)
            # Описание: все Nodes которые содержат в себе QtWidgets.QWidget() при 3-х разовом удалении

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            node_items = [item for item in self.items() if isinstance(item, Node)]

            # [Ctrl + A]
            if event.key() == QtCore.Qt.Key.Key_A:
                all_selected = len(self.selectedItems()) == len(node_items)
                for item in node_items:
                    item.setSelected(not all_selected)

            # [Ctrl + N]
            if event.key() == QtCore.Qt.Key.Key_N:

                match extra_message():

                    case QtWidgets.QMessageBox.StandardButton.Save:
                        file_message(scene=self, mode=QtWidgets.QFileDialog.AcceptMode.AcceptSave)

                    case QtWidgets.QMessageBox.StandardButton.Discard:
                        for item in node_items:
                            item.delete()

                    case QtWidgets.QMessageBox.StandardButton.Cancel:
                        pass

        return super().keyPressEvent(event)

    # ---------------------------------------------------------------------------------------------------------------------#
    def load_scene(self, json_path: str) -> None:
        """
        Load the scene from the .json file.
        """

        with open(json_path) as f:
            data = json.load(f)

        if data:
            node_lookup = {}  # A dictionary of nodes, by uuids

            # Add the nodes
            for n in data["nodes"]:
                if n["type"] in GLOBAL_IMPORTS.keys():
                    info = GLOBAL_IMPORTS[n["type"]]
                    node = self.call_node_class(name=n["type"], class_name=info["class"])
                    node.uuid = n["uuid"]
                    node.value = n["value"]
                    pos = QtCore.QPointF(n["x"], n["y"])

                    self.create_node(node, pos)

                    node_lookup[node.uuid] = node

                else:
                    print(f"{n['type']} module is not found.")
                    return

            # Add the connections
            for c in data["connections"]:
                if node_lookup:
                    start_pin = node_lookup[c["start_uuid"]].get_pin(c["start_pin"])
                    end_pin = node_lookup[c["end_uuid"]].get_pin(c["end_pin"])

                    connection = Connection()
                    connection.set_start_pin(start_pin)
                    connection.set_end_pin(end_pin)
                    connection.update_start_and_end_pos()
                    self.addItem(connection)

    def save_scene(self, json_path: str) -> None:
        """
        Save the scene to the .json file.
        """

        json_scene = {"nodes": [], "connections": []}

        for item in self.items():

            # Nodes
            if isinstance(item, Node):
                pos = item.pos().toPoint()

                node = {
                    "type": type(item).__name__,
                    "x": pos.x(),
                    "y": pos.y(),
                    "uuid": str(item.uuid),
                    "value": item.value,
                }

                json_scene["nodes"].append(node)

            # Connections
            if isinstance(item, Connection):
                connection = {
                    "start_uuid": str(item.start_pin.node.uuid),
                    "end_uuid": str(item.end_pin.node.uuid),
                    "start_pin": item.start_pin.name,
                    "end_pin": item.end_pin.name,
                }

                json_scene["connections"].append(connection)

        with open(json_path, "w") as f:
            json.dump(json_scene, f, indent=4)
