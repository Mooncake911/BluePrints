import importlib.util
import inspect
import logging
import sys
from pathlib import Path
import qdarktheme

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QMenu, QFileDialog,
                               QApplication)


from node_editor.gui.node_list import NodeList
from node_editor.gui.node_widget import NodeWidget

logging.basicConfig(level=logging.DEBUG)


class NodeEditor(QMainWindow):
    OnProjectPathUpdate = QtCore.Signal(Path)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = None
        self.imports = None

        self.setWindowTitle("Simple Node Editor")
        settings = QtCore.QSettings("Silk Road", "IoT Editor")
        self.create_menus()

        # Layouts
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 5, 0)

        # Widgets
        self.node_list = NodeList(self)
        left_widget = QWidget()
        self.splitter = QSplitter()
        self.node_widget = NodeWidget(self)

        # Add Widgets to layouts
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(self.node_widget)
        left_widget.setLayout(left_layout)
        left_layout.addWidget(self.node_list)
        main_layout.addWidget(self.splitter)

        # Add nodes to widgets
        self.example_project_path = Path('node_editor/example')
        self.load_nodes()

        # Restore GUI from last state
        if settings.contains("geometry"):
            self.restoreGeometry(settings.value("geometry"))
            s = settings.value("splitterSize")
            self.splitter.restoreState(s)

    def create_menus(self):
        # "File" menu
        file_menu = QMenu("File")
        self.menuBar().addMenu(file_menu)

        load_action = QtGui.QAction("Load Project", self)
        load_action.triggered.connect(self.load_project)
        file_menu.addAction(load_action)

        save_action = QtGui.QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        # "Help" menu
        help_menu = QMenu("Help")
        self.menuBar().addMenu(help_menu)

        github_action = QtGui.QAction("Visit GitHub", self)
        github_action.triggered.connect(self.visit_github)
        help_menu.addAction(github_action)

    def visit_github(self):
        url = QtCore.QUrl("https://github.com/Mooncake911/BluePrints/blob/master/resources/docs/shortcuts.md")
        QtGui.QDesktopServices.openUrl(url)

    def save_project(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("JSON files (*.json)")
        default_filename = "projects"
        file_path, _ = file_dialog.getSaveFileName(self, "Save json file", default_filename, "Json Files (*.json)")
        if file_path:
            self.node_widget.save_project(file_path)

    def load_nodes(self):
        self.imports = {}

        def load_module(file):
            try:
                spec = importlib.util.spec_from_file_location(file.stem, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(module):
                    if not name.endswith('_Node'):
                        continue
                    if inspect.isclass(obj):
                        # print(file.parts[1:-1])
                        self.imports[obj.__name__] = {"parent": file.parent.name, "class": obj, "module": module}
            except Exception as e:
                print(f"Error loading module {file}: {e}")

        for f in self.example_project_path.rglob("*.py"):
            load_module(f)

        self.node_list.update_project(self.imports, self.example_project_path)

    def load_project(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setDefaultSuffix("json")
        dialog.setNameFilter("JSON files (*.json)")
        if dialog.exec():
            project_path = Path(dialog.selectedFiles()[0])
            self.node_widget.load_scene(project_path, self.imports)
        else:
            return

    def closeEvent(self, event):
        self.settings = QtCore.QSettings("python_node_interface-editor", "NodeEditor")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterSize", self.splitter.saveState())
        QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QtGui.QIcon("resources/img/app.ico"))
    qdarktheme.setup_theme('dark')  # 'auto', 'light'

    launcher = NodeEditor()
    launcher.show()
    app.exec()
    sys.exit()
