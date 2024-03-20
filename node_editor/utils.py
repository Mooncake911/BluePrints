import os

from PySide6.QtWidgets import QMessageBox, QFileDialog


_default_folder = "projects"


def get_name(file):
    script_path = os.path.abspath(file)
    file_name = os.path.splitext(os.path.basename(script_path))[0]
    return file_name.split("_")[0]


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


def file_message(scene, mode: QFileDialog.AcceptMode) -> None:
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
            scene.save_scene(project_path)

    if mode == file_dialog.AcceptMode.AcceptOpen:
        project_path, _ = file_dialog.getOpenFileName(file_dialog, "Open json file", _default_folder,
                                                      "Json Files (*.json)")
        if project_path:
            scene.load_scene(project_path)
