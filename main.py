import sys
from pathlib import Path
import qdarktheme

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QMenu, QFileDialog,
                               QApplication)


from node_editor.gui.node_list import NodeList
from node_editor.gui.node_widget import NodeWidget


class NodeEditor(QMainWindow):
    OnProjectPathUpdate = QtCore.Signal(Path)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IoT Node Editor")

        self.node_list = NodeList(self)  # QTreeWidget
        self.node_widget = NodeWidget(self)

        self.create_menus()
        self.create_editor()

    def create_menus(self):
        """ Create the menus """
        def visit_github():
            url = QtCore.QUrl("https://github.com/Mooncake911/BluePrints/blob/master/resources/docs/shortcuts.md")
            QtGui.QDesktopServices.openUrl(url)

        # File menu
        file_menu = QMenu("File")
        self.menuBar().addMenu(file_menu)

        load_action = QtGui.QAction("Load Project", self)
        load_action.triggered.connect(self.load_project)
        file_menu.addAction(load_action)

        save_action = QtGui.QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        # Help menu
        help_menu = QMenu("Help")
        self.menuBar().addMenu(help_menu)

        github_action = QtGui.QAction("Visit GitHub", self)
        github_action.triggered.connect(visit_github)
        help_menu.addAction(github_action)

    def create_editor(self):
        """ Create the editor """
        # Left widget
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.node_list)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget.setLayout(left_layout)

        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.node_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(main_layout)

        # Combine (Main, Left)
        splitter = QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(main_widget)
        splitter.setContentsMargins(7, 7, 7, 7)
        self.setCentralWidget(splitter)

    def save_project(self):
        """ Save the project to .json """
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("JSON files (*.json)")
        default_filename = "projects"
        file_path, _ = file_dialog.getSaveFileName(self, "Save json file", default_filename, "Json Files (*.json)")
        if file_path:
            self.node_widget.save_project(file_path)

    def load_project(self):
        """ Load the project from .json """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setDefaultSuffix("json")
        dialog.setNameFilter("JSON files (*.json)")
        if dialog.exec():
            project_path = Path(dialog.selectedFiles()[0])
            self.node_widget.load_scene(project_path, self.node_list.imports)
        else:
            return

    def closeEvent(self, event):
        QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QtGui.QIcon("resources/img/app.ico"))
    qdarktheme.setup_theme('dark')  # 'auto', 'light'

    launcher = NodeEditor()
    launcher.show()
    app.exec()
    sys.exit()
