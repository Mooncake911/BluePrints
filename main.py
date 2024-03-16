import sys
import qdarktheme
from functools import partial

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (QMainWindow, QWidget, QSplitter, QMenu, QFileDialog, QApplication)


from node_editor.gui import NodeList, View


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Node Editor")

        # Left widget
        self.node_list = NodeList()
        # Main widget
        self.view = View()

        self.create_menus()
        self.create_editor()

    def create_menus(self):
        """ Create the menu for editor """
        def visit_github():
            url = QtCore.QUrl("https://github.com/Mooncake911/BluePrints/blob/master/resources/docs/shortcuts.md")
            QtGui.QDesktopServices.openUrl(url)

        menu = self.menuBar()

        # ~ File menu
        file_menu = QMenu("File")
        menu.addMenu(file_menu)

        save_action = QtGui.QAction("Save Project", file_menu)
        save_action.triggered.connect(lambda: self.json_project(mode="save"))
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        load_action = QtGui.QAction("Open Project", file_menu)
        load_action.triggered.connect(lambda: self.json_project(mode="open"))
        load_action.setShortcut("Ctrl+O")
        file_menu.addAction(load_action)

        # def theme_action_triggered(theme_):
        #     def on_triggered():
        #         qdarktheme.setup_theme(theme_)
        #
        #     return on_triggered

        # ~ View menu
        view_menu = QMenu("View")
        menu.addMenu(view_menu)
        view_submenu = view_menu.addMenu("Theme")

        themes = ["auto", "light", "dark"]
        for theme in themes:
            action = QtGui.QAction(theme.capitalize(), view_submenu)
            action.triggered.connect(partial(qdarktheme.setup_theme, theme))  # theme_action_triggered(theme_)
            view_submenu.addAction(action)

        # ~ Help menu
        help_menu = QMenu("Help")
        menu.addMenu(help_menu)

        github_action = QtGui.QAction("Visit GitHub", help_menu)
        github_action.triggered.connect(visit_github)
        github_action.setShortcut("Ctrl+F1")
        help_menu.addAction(github_action)

    def create_editor(self):
        """ Create the editor """
        splitter = QSplitter()
        splitter.addWidget(self.node_list)
        splitter.addWidget(self.view)
        splitter.setContentsMargins(7, 7, 7, 7)
        self.setCentralWidget(splitter)

    def json_project(self, mode: str = None):
        """ Save/Load the project to .json """
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("JSON files (*.json)")

        default_filename = "projects"

        if mode.lower() == "save":
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            project_path, _ = file_dialog.getSaveFileName(self, f"{mode.capitalize()} json file", default_filename,
                                                          "Json Files (*.json)")
            if project_path:
                self.node_list.save_scene(self.view.node_scene, project_path)

        if mode.lower() == "open":
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
            project_path, _ = file_dialog.getOpenFileName(self, f"{mode.capitalize()} json file", default_filename,
                                                          "Json Files (*.json)")
            if project_path:
                self.node_list.load_scene(self.view.node_scene, project_path)

    def closeEvent(self, event):
        QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QtGui.QIcon("resources/img/app.ico"))
    qdarktheme.setup_theme('dark', corner_shape="rounded")  # Adefault

    launcher = Launcher()
    launcher.show()

    app.exec()
    sys.exit()
