import sys
import qdarktheme
from functools import partial

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import (QMainWindow, QMenu, QApplication)

from windows import Windows
from db.redis_db import redis_manager


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Node Editor")

        self.windows = Windows()
        self.setCentralWidget(self.windows)

        self.create_menus()

    @QtCore.Slot()
    def visit_github(self):
        url = QtCore.QUrl("https://github.com/Mooncake911/BluePrints/blob/master/resources/docs/shortcuts.md")
        QtGui.QDesktopServices.openUrl(url)

    @QtCore.Slot(str)
    def change_theme(self, theme):
        qdarktheme.setup_theme(theme=theme, corner_shape="rounded")

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

        create_action(_text_="Save Project", _menu_=file_menu, _key_="Ctrl+S",
                      _slot_=self.windows.node_editor.save_project)

        create_action(_text_="Open Project", _menu_=file_menu, _key_="Ctrl+O",
                      _slot_=self.windows.node_editor.load_project)

        file_menu.addSeparator()

        create_action(_text_="Exit", _menu_=file_menu, _slot_=self.close, _key_="Alt+F4")

        # ~ View menu
        view_menu = QMenu("View")
        menu.addMenu(view_menu)
        view_submenu = view_menu.addMenu("Theme")

        themes = ["auto", "light", "dark"]
        for theme in themes:
            create_action(_text_=theme.capitalize(), _menu_=view_submenu,
                          _slot_=partial(self.change_theme, theme))

        # ~ Help menu
        help_menu = QMenu("Help")
        menu.addMenu(help_menu)

        create_action(_text_="Visit GitHub", _menu_=help_menu, _slot_=self.visit_github, _key_="Ctrl+F1")

    def closeEvent(self, event):
        self.windows.closeEvent(event)
        redis_manager.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QtGui.QIcon("resources/icons/app.ico"))
    qdarktheme.setup_theme(theme='dark', corner_shape="rounded")  # default

    launcher = Launcher()
    launcher.show()

    app.exec()
    sys.exit()
