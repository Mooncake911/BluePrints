# Helpful method for

import json
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox, QFileDialog
from node_editor.attributes import Node, Connection

_default_folder = "projects"


def extra_message():
    """
    Warning message box for user, who can lose the unsaved result.
    :return: Save, Discard or Cancel button.
    """
    msg_box = QMessageBox()
    msg_box.setText("The project has been modified.")
    msg_box.setInformativeText("Do you want to save your changes?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Save
                               | QMessageBox.StandardButton.Discard
                               | QMessageBox.StandardButton.Cancel)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Save)
    return msg_box.exec_()


def file_message(scene, mode) -> None:
    """
    Calls when want to save/open the scene to .json file.

    :param scene: The ViewScene() from view_scene.py
    :param mode: QFileDialog.AcceptMode.AcceptSave or QFileDialog.AcceptMode.AcceptOpen
    """
    global _default_folder

    file_dialog = QFileDialog()
    file_dialog.setDefaultSuffix("json")
    file_dialog.setNameFilter("JSON files (*.json)")
    file_dialog.setAcceptMode(mode)

    if mode == file_dialog.AcceptMode.AcceptSave:
        project_path, _ = file_dialog.getSaveFileName(file_dialog, "Save json file", _default_folder,
                                                      "Json Files (*.json)")
        if project_path:
            save_scene(scene, project_path)

    if mode == file_dialog.AcceptMode.AcceptOpen:
        project_path, _ = file_dialog.getOpenFileName(file_dialog, "Open json file", _default_folder,
                                                      "Json Files (*.json)")
        if project_path:
            # scene.load_scene(node_list.imports, project_path)
            pass


def load_scene(scene, imports, json_path: str) -> None:
    """
    Load the scene from the .json file.

    :param scene: The ViewScene() from view_scene.py
    :param imports: The NodeList().imports from node_list.py
    :param json_path: The json file path
    """

    with open(json_path) as f:
        data = json.load(f)

    if data:
        node_lookup = {}  # A dictionary of nodes, by uuids

        # Add the nodes
        for n in data["nodes"]:
            if n["type"] in imports.keys():
                info = imports[n["type"]]
                node = info["class"]()
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
                scene.addItem(connection)

                if start_pin:
                    connection.set_start_pin(start_pin)
                if end_pin:
                    connection.set_end_pin(end_pin)

                connection.update_start_and_end_pos()


def save_scene(scene, json_path: str) -> None:
    """
    Save the scene to the .json file.

    :param scene: The ViewScene() from view_scene.py
    :param json_path: The json file path
    """

    json_scene = {"nodes": [], "connections": []}

    for item in scene.items():

        # Nodes
        if isinstance(item, Node):
            pos = item.pos().toPoint()
            obj_type = type(item).__name__

            node = {
                "type": obj_type,
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
