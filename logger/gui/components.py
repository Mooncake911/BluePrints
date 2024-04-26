from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QCompleter)
from PySide6.QtGui import Qt, QColor, QFont, QIntValidator
from PySide6.QtCore import QStringListModel

import serial.tools.list_ports as find_ports
from serial.tools.list_ports_common import ListPortInfo


class InnerHLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, label_text: str, button_labels: list[str], button_funcs,
                 suggestions: set, validator=None):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.label_text = label_text
        self.button_labels = button_labels
        self.button_funcs = button_funcs
        self.suggestions = suggestions
        self.validator = validator

        self.label = QLabel()
        self.completer = QCompleter()
        self.line_edit = QLineEdit()
        self.button = QPushButton()
        self.init_ui()

        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def init_ui(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.completer.setModel(QStringListModel(self.suggestions))
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.line_edit.setCompleter(self.completer)
        self.line_edit.setValidator(self.validator)
        self.line_edit.textChanged.connect(self.check_button_state)

        self.button.setEnabled(False)
        self.button.setText(self.button_labels[0])
        self.button.setFixedWidth(self._button_width)
        self.button.clicked.connect(self.execute)

    def check_button_state(self, text):
        if bool(text):
            self.button.setEnabled(True)

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

        self.layout.addLayout(
            InnerHLayout(label_text="Port:",
                         button_labels=["Connect", "Disconnect"],
                         button_funcs=[self.connect_to_port, self.disconnected_from_port],
                         suggestions=self.ports_history(),
                         validator=self.port_validator())
        )

        self.layout.addLayout(
            InnerHLayout(label_text="Topic:",
                         button_labels=["Subscribe", "Unsubscribe"],
                         button_funcs=[self.subscribe_to_topic, self.unsubscribe_from_topic],
                         suggestions=self.topics_history())
        )

        self.layout.addLayout(
            InnerHLayout(label_text="Message:",
                         button_labels=["Publish"],
                         button_funcs=[self.publish_message],
                         suggestions=self.message_history())
        )

        self.setLayout(self.layout)

    # /// --- ~ Buttons functions ~ --- \\\ #
    def connect_to_port(self, port) -> None:
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Connected: {port}\n")

    def disconnected_from_port(self, port) -> None:
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Disconnected: {port}\n")

    def subscribe_to_topic(self, topic) -> None:
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Subscribe: {topic}\n")

    def unsubscribe_from_topic(self, topic) -> None:
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Unsubscribe: {topic}\n")

    def publish_message(self, message) -> None:
        self.logger.setTextColor(QColor(255, 255, 255))
        self.logger.append(f"Published: {message}\n")

    # /// --- ~ Histories ~ --- \\\ #
    @staticmethod
    def ports_history() -> set[ListPortInfo]:
        ports = find_ports.comports()
        # if ports:
        #     for port, desc, hwid in sorted(ports):
        #         print(f"Порт: {port}, Описание: {desc}, Аппаратный ID: {hwid}")
        # else:
        #     print("COM-порты не найдены.")
        return set(ports)

    @staticmethod
    def topics_history():
        return set()

    @staticmethod
    def message_history() -> set[str]:
        return {"привет", "пока"}

    # /// --- ~ Validators ~ --- \\\ #
    @staticmethod
    def port_validator():
        validator = QIntValidator()
        validator.setRange(0, 65535)
        return validator
