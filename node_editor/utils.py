import os
import json

from PySide6 import QtCore, QtWidgets

from node_editor.attributes import Node, Connection
from node_editor.gui.node_list import GLOBAL_IMPORTS

_default_folder = "projects"


def get_name(file):
    script_path = os.path.abspath(file)
    file_name = os.path.splitext(os.path.basename(script_path))[0]
    return file_name.split("_")[0]


def extra_message(scene):
    """
    Warning message box for user, who can lose the unsaved result.

    :param scene: The ViewScene() from view_scene.py
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
            file_message(scene=scene, mode=QtWidgets.QFileDialog.AcceptMode.AcceptSave)

        case QtWidgets.QMessageBox.StandardButton.Discard:
            scene.clear()

        case QtWidgets.QMessageBox.StandardButton.Cancel:
            pass


def file_message(scene, mode: QtWidgets.QFileDialog.AcceptMode) -> None:
    """
    Calls when want to save/open the scene to .json file.

    :param scene: The ViewScene() from view_scene.py
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
            save_scene(scene=scene, json_path=project_path)

    if mode == file_dialog.AcceptMode.AcceptOpen:
        project_path, _ = file_dialog.getOpenFileName(file_dialog, "Open json file", _default_folder,
                                                      "Json Files (*.json)")
        if project_path:
            load_scene(scene=scene, json_path=project_path)


def load_scene(scene, json_path: str) -> None:
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
                node = scene.call_node_class(name=n["type"], class_name=info["class"])
                node.uuid = n["uuid"]
                node.value = n["value"]
                pos = QtCore.QPointF(n["x"], n["y"])

                scene.create_node(node, pos)

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
                scene.addItem(connection)


def save_scene(scene, json_path: str) -> None:
    """
    Save the scene to the .json file.
    """

    json_scene = {"nodes": [], "connections": []}

    for item in scene.items():

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
