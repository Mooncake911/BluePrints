from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression


class JsonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(JsonSyntaxHighlighter, self).__init__(parent)

        self.highlightingRules = []

        # Highlight json keys
        self.addHighlight(hex_color="#800080", str_expression=r'(".*?")\s*:', font=QFont.Bold)

        # Highlight true и false
        self.addHighlight(hex_color="#FFA500", str_expression=r'\b(true|false)\b')

        # Highlight numbers
        self.addHighlight(hex_color="#00daff", str_expression=r':\s*(-?\d*\.?\d+)')

    def addHighlight(self, hex_color, str_expression, font=False):
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(hex_color))
        text_format.setFontWeight(font)
        self.highlightingRules.append((str_expression, text_format))

    def highlightBlock(self, text):
        for pattern, text_format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(1), match.capturedLength(1), text_format)


class NodeInfo(QWidget):
    def __init__(self, text="Text"):
        super().__init__()
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        JsonSyntaxHighlighter(self.text_edit.document())
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(text)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
