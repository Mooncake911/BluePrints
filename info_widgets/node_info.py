from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class NodeInfo(QWidget):
    def __init__(self, text="Text"):
        super().__init__()
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit(text)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
