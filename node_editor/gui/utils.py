import json
import uuid

from PySide6 import QtCore, QtWidgets

from .attributes import Node, Connection, NodeStatus
from .node_list import NODE_IMPORTS


_default_folder = "projects"


class Utils:
    def __init__(self, scene):
        self.scene = scene

    def create_node(self, node, pos):
        node.init_widget()
        node.setPos(pos)
        self.scene.addItem(node)

    def extra_message(self):
        """
        Warning message box for user, who can lose the unsaved result.
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText("The project has been modified.")
        msg_box.setInformativeText("Do you want to save your changes?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Save
                                   | QtWidgets.QMessageBox.StandardButton.Discard
                                   | QtWidgets.QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Save)

        match msg_box.exec_():

            case QtWidgets.QMessageBox.StandardButton.Save:
                self.file_message(mode=QtWidgets.QFileDialog.AcceptMode.AcceptSave)

            case QtWidgets.QMessageBox.StandardButton.Discard:
                self.scene.clear()

            case QtWidgets.QMessageBox.StandardButton.Cancel:
                pass

    def file_message(self, mode: QtWidgets.QFileDialog.AcceptMode) -> None:
        """
        Calls when want to save/open the scene to .json file.

        :param mode: QFileDialog.AcceptMode.AcceptSave or QFileDialog.AcceptMode.AcceptOpen
        """
        global _default_folder

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.setAcceptMode(mode)

        if mode == file_dialog.AcceptMode.AcceptSave:
            project_path, _ = file_dialog.getSaveFileName(file_dialog, "Save json file", _default_folder,
                                                          "Json Files (*.json)")
            if project_path:
                self.save_scene(json_path=project_path)

        if mode == file_dialog.AcceptMode.AcceptOpen:
            project_path, _ = file_dialog.getOpenFileName(file_dialog, "Open json file", _default_folder,
                                                          "Json Files (*.json)")
            if project_path:
                self.load_scene(json_path=project_path)

    def load_scene(self, json_path: str) -> None:
        """
        Load the scene from the .json file.
        """

        with open(json_path) as f:
            data = json.load(f)

        if data:
            node_list = {}  # A dictionary of nodes, by uuids

            # Add the nodes
            for n in data["nodes"]:
                if n["type"] in NODE_IMPORTS.keys():
                    class_name = NODE_IMPORTS[n["type"]]
                    node = class_name["class"](name=n["type"], scene=self.scene)

                    node.uuid = uuid.uuid4()  # set new uuid
                    pos = QtCore.QPointF(n["x"], n["y"])

                    for key in ["id", "value", "index"]:
                        try:
                            setattr(node, key, n[key])
                        except KeyError:
                            pass

                    node_list[n["uuid"]] = node
                    self.create_node(node, pos)

                else:
                    print(f"{n['type']} module is not found.")
                    return

            # Add the connections
            for c in data["connections"]:
                if node_list:
                    start_pin = node_list[c["start_uuid"]].get_start_pin(c["start_pin"])
                    end_pin = node_list[c["end_uuid"]].get_end_pin(c["end_pin"])

                    connection = Connection()
                    connection.set_start_pin(start_pin)
                    connection.set_end_pin(end_pin)
                    connection.update_start_and_end_pos()
                    self.scene.addItem(connection)

    def save_scene(self, json_path: str) -> None:
        """
        Save the scene to the .json file.
        """

        json_scene = {"nodes": [], "connections": []}

        for item in self.scene.items():

            # Nodes
            if isinstance(item, Node):
                pos = item.pos().toPoint()

                node = {
                    "type": item.name,
                    "x": pos.x(),
                    "y": pos.y(),
                    "uuid": str(item.uuid),
                }
                if item.value:
                    node["value"] = item.value
                if item.index:
                    node["index"] = item.index
                if item.id:
                    node["id"] = item.id

                json_scene["nodes"].append(node)

                # TODO: сделать нормальные предупреждения ::
                if item.status == NodeStatus.ERROR:
                    print('NODE ERROR WAS FOUND')
                if item.status == NodeStatus.WARNING:
                    print('NODE WARNING WAS FOUND')

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
