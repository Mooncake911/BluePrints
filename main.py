import sys
import qdarktheme
from functools import partial

from PySide6 import QtGui
from PySide6.QtWidgets import (QMainWindow, QWidget, QSplitter, QMenu, QApplication, QFileDialog)

from node_editor.gui import NodeList, View, ViewScene
from node_editor.utils import visit_github, file_message, extra_message


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Node Editor")

        # Create scene
        self.scene = ViewScene()

        # Left widget
        self.node_list = NodeList()

        # Main widget
        self.view = View(self.scene)

        self.create_menus()
        self.create_editor()

    def create_menus(self):
        """ Create the menu for editor """

        def create_action(_text_, _menu_, _slot_, _key_: str = False):
            """ Helper function to save typing when populating menus
                with action.
            """
            _action_ = QtGui.QAction(_text_, self)
            _action_.triggered.connect(_slot_)
            _action_.setShortcut(_key_)
            _menu_.addAction(_action_)
            return _action_

        menu = self.menuBar()

        # ~ File menu
        file_menu = QMenu("File")
        menu.addMenu(file_menu)

        create_action(_text_="Save Project", _menu_=file_menu,
                      _slot_=partial(file_message, scene=self.scene, mode=QFileDialog.AcceptMode.AcceptSave),
                      _key_="Ctrl+S")

        create_action(_text_="Open Project", _menu_=file_menu,
                      _slot_=partial(file_message, scene=self.scene, mode=QFileDialog.AcceptMode.AcceptOpen),
                      _key_="Ctrl+O")

        file_menu.addSeparator()

        create_action(_text_="Exit", _menu_=file_menu, _slot_=self.close, _key_="Alt+F4")

        # ~ View menu
        view_menu = QMenu("View")
        menu.addMenu(view_menu)
        view_submenu = view_menu.addMenu("Theme")

        themes = ["auto", "light", "dark"]
        for theme in themes:
            create_action(_text_=theme.capitalize(), _menu_=view_submenu,
                          _slot_=partial(qdarktheme.setup_theme, theme=theme, corner_shape="rounded"))

        # ~ Help menu
        help_menu = QMenu("Help")
        menu.addMenu(help_menu)

        create_action(_text_="Visit GitHub", _menu_=help_menu, _slot_=visit_github, _key_="Ctrl+F1")

    def create_editor(self):
        """ Create the editor """
        splitter = QSplitter()
        splitter.addWidget(self.node_list)
        splitter.addWidget(self.view)
        splitter.setContentsMargins(7, 7, 7, 7)
        self.setCentralWidget(splitter)

    def closeEvent(self, event):
        if self.scene.items():
            extra_message(self.scene)
        QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QtGui.QIcon("resources/img/app.ico"))
    qdarktheme.setup_theme(theme='dark', corner_shape="rounded")  # default

    launcher = Launcher()
    launcher.show()

    app.exec()
    sys.exit()
