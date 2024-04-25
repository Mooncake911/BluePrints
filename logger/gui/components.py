from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTextEdit, QCompleter)
from PySide6.QtGui import Qt, QColor, QFont
from PySide6.QtCore import QStringListModel

import serial.tools.list_ports as find_ports


class InnerHLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, label_text: str, button_labels: list[str], button_funcs, suggestions: set):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.label_text = label_text
        self.button_labels = button_labels
        self.button_funcs = button_funcs
        self.suggestions = suggestions

        self.label = QLabel()
        self.completer = QCompleter()
        self.line_edit = QLineEdit()
        self.button = QPushButton()
        self.ui()

        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def ui(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.completer.setModel(QStringListModel(self.suggestions))
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.line_edit.setCompleter(self.completer)

        self.button.setText(self.button_labels[0])
        self.button.setFixedWidth(self._button_width)
        self.button.clicked.connect(self.execute)

    def execute(self):
        new_input = self.line_edit.text()

        # Remember user input
        self.suggestions.add(new_input)
        self.completer.setModel(QStringListModel(self.suggestions))

        # Do current button functon and set new button text after it
        button_index = self.button_labels.index(self.button.text())
        current_button_func = self.button_funcs[button_index % len(self.button_labels)]
        current_button_func(new_input)
        new_button_text = self.button_labels[(button_index + 1) % len(self.button_labels)]
        self.button.setText(new_button_text)


class InputLogWidget(QWidget):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.layout = QVBoxLayout()

        self.layout.addLayout(InnerHLayout(label_text="Port:",
                                           button_labels=["Connect", "Disconnect"],
                                           button_funcs=[self.connect_to_port, self.disconnected_from_port],
                                           suggestions=self.list_serial_ports()))

        self.layout.addLayout(InnerHLayout(label_text="Topic:",
                                           button_labels=["Subscribe", "Unsubscribe"],
                                           button_funcs=[self.subscribe_to_topic, self.unsubscribe_from_topic],
                                           suggestions=self.list_serial_ports()))

        self.layout.addLayout(InnerHLayout(label_text="Message:",
                                           button_labels=["Publish"],
                                           button_funcs=[self.publish_message],
                                           suggestions=self.message_history()))

        self.setLayout(self.layout)

    def connect_to_port(self, port):
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Connected: {port}\n")

    def disconnected_from_port(self, port):
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Disconnected: {port}\n")

    def subscribe_to_topic(self, topic):
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Subscribe: {topic}\n")

    def unsubscribe_from_topic(self, topic):
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Unsubscribe: {topic}\n")

    def publish_message(self, message):
        self.logger.setTextColor(QColor(255, 255, 255))
        self.logger.append(f"Published: {message}\n")

    @staticmethod
    def list_serial_ports():
        ports = find_ports.comports()
        # if ports:
        #     for port, desc, hwid in sorted(ports):
        #         print(f"Порт: {port}, Описание: {desc}, Аппаратный ID: {hwid}")
        # else:
        #     print("COM-порты не найдены.")
        return set(ports)

    @staticmethod
    def list_serial_topics():
        return {}

    @staticmethod
    def message_history():
        return {"привет", "пока"}


class OutputLogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.logger = QTextEdit()
        self.logger.setFont(QFont("Arial", 10))
        self.logger.setReadOnly(True)
        self.logger.setPlaceholderText('Log Message')
        self.layout.addWidget(self.logger)

        self.button = QPushButton('Clear')
        self.button.clicked.connect(self.logger.clear)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
