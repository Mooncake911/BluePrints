from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QCompleter, QSpacerItem, QSizePolicy, QStyle)
from PySide6.QtGui import Qt, QColor, QIntValidator
from PySide6.QtCore import QStringListModel

import serial.tools.list_ports as find_ports
from serial.tools.list_ports_common import ListPortInfo


class CustomMenuLayout(QHBoxLayout):
    _label_width = 70
    _layout_space = 20

    def __init__(self, button_func):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.label = QLabel()
        self.label.setText("Reload:")
        self.label.setFixedWidth(self._label_width)

        self.button = QPushButton()
        self.button.setFixedSize(30, 30)
        icon = self.button.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.button.setIcon(icon)
        self.button.setIconSize(self.button.size())
        self.button.clicked.connect(button_func)
        self.button.clicked.connect(self.execute)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.addWidget(self.label)
        self.addWidget(self.button)
        self.addItem(self.spacer)

    def execute(self):
        """ Анимация нажатия кнопки перезагрузки """
        pass


class CustomInputLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, label_text: str, button_labels: list[str], button_funcs, validator=None):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.history = []
        self.label_text = label_text
        self.button_labels = button_labels
        self.button_funcs = button_funcs

        self.label = QLabel()
        self.completer = QCompleter()
        self.validator = validator
        self.line_edit = QLineEdit()
        self.button = QPushButton()
        self.init_ui()

        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def renew_history(self, history):
        self.history = history
        if self.history:
            self.line_edit.setText(self.history[0])
            self.completer.setModel(QStringListModel(self.history))

    def init_ui(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.line_edit.setCompleter(self.completer)
        self.line_edit.setValidator(self.validator)
        self.line_edit.textChanged.connect(self.check_button_state)

        if not self.line_edit.text():
            self.button.setEnabled(False)
        self.button.setText(self.button_labels[0])
        self.button.setFixedWidth(self._button_width)
        self.button.clicked.connect(self.execute)

    def check_button_state(self, text):
        if bool(text):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def execute(self):
        user_input = self.line_edit.text()

        # Remember user input
        if user_input not in self.history:
            self.history.append(user_input)
            self.completer.setModel(QStringListModel(self.history))

        # Do current button functon and set new button text after it
        button_index = self.button_labels.index(self.button.text())
        current_button_func = self.button_funcs[button_index % len(self.button_labels)]
        current_button_func(user_input)
        new_button_text = self.button_labels[(button_index + 1) % len(self.button_labels)]
        self.button.setText(new_button_text)


class ConsoleInput(QWidget):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.layout = QVBoxLayout()

        self.menu_layout = CustomMenuLayout(button_func=self.execute)

        self.port_layout = CustomInputLayout(label_text="Port:",
                                             button_labels=["Connect", "Disconnect"],
                                             button_funcs=[self.connect_to_port, self.disconnected_from_port])

        self.topic_layout = CustomInputLayout(label_text="Topic:",
                                              button_labels=["Subscribe", "Unsubscribe"],
                                              button_funcs=[self.subscribe_to_topic, self.unsubscribe_from_topic])

        self.message_layout = CustomInputLayout(label_text="Message:",
                                                button_labels=["Publish"],
                                                button_funcs=[self.publish_message])
        self.execute()

        self.layout.addLayout(self.menu_layout)
        self.layout.addLayout(self.port_layout)
        self.layout.addLayout(self.topic_layout)
        self.layout.addLayout(self.message_layout)

        self.setLayout(self.layout)

    def execute(self):
        # Renew suggestions
        self.port_layout.renew_history(self.ports_history())
        self.topic_layout.renew_history(self.topics_history())
        self.message_layout.renew_history(self.message_history())

        self.logger.setTextColor(QColor(255, 255, 255))
        self.logger.append(f"~ --- New session --- ~")

    # /// --- ~ Buttons functions ~ --- \\\ #
    def connect_to_port(self, port) -> None:
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Connected: {port}")

    def disconnected_from_port(self, port) -> None:
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Disconnected: {port}")

    def subscribe_to_topic(self, topic) -> None:
        self.logger.setTextColor(QColor(0, 255, 0))
        self.logger.append(f"Subscribe: {topic}")

    def unsubscribe_from_topic(self, topic) -> None:
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Unsubscribe: {topic}")

    def publish_message(self, message) -> None:
        self.logger.setTextColor(QColor(255, 255, 255))
        self.logger.append(f"Published: {message}")

    # /// --- ~ Histories ~ --- \\\ #
    @staticmethod
    def ports_history() -> list[ListPortInfo]:
        # TODO: добавить то что в принтах в нормальные логи
        ports_list = []
        ports = find_ports.comports()
        if ports:
            for port, desc, hwid in sorted(ports):
                ports_list.append(port)
                print(f"Порт: {port}, Описание: {desc}, Аппаратный ID: {hwid}")
        else:
            print("COM-порты не найдены.")
        return ports_list

    @staticmethod
    def topics_history() -> list[str]:
        return ['None']

    @staticmethod
    def message_history() -> list[str]:
        return ["привет", "пока"]

    # /// --- ~ Validators ~ --- \\\ #
    @staticmethod
    def port_validator():
        validator = QIntValidator()
        validator.setRange(0, 65535)
        return validator
