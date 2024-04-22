from PySide6.QtWidgets import QSplitter, QTableWidget
from PySide6.QtGui import Qt


class Logger(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Vertical)

        table1 = QTableWidget()
        table1.setColumnCount(2)
        table1.setHorizontalHeaderLabels(['Name', 'Value'])

        table2 = QTableWidget()
        table2.setColumnCount(2)
        table2.setHorizontalHeaderLabels(['Name', 'Value'])

        self.addWidget(table1)
        self.addWidget(table2)
