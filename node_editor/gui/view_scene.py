from PySide6 import QtCore, QtGui, QtWidgets
from node_editor.attributes import Node
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

    def dragMoveEvent(self, event):
        """
        This method is called when a drag and drop event enters the view.
        It checks if the mime data format is "text/plain" and accepts or ignores the event accordingly.
        """
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        This method is called when a drag and drop event is dropped onto the view.
        It retrieves the name of the dropped node from the mime data and emits a signal to request the creation of the
        corresponding node.
        """
        node = event.mimeData().item.class_name
        if node:
            self.create_node(node(), event.scenePos())

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
            return True

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            node_items = [item for item in self.items() if isinstance(item, Node)]

            # [Ctrl + A]
            if event.key() == QtCore.Qt.Key.Key_A:
                all_selected = len(self.selectedItems()) == len(node_items)
                for item in node_items:
                    item.setSelected(not all_selected)
                return True

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

                return True
