from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QComboBox)
from PySide6.QtGui import QColor

import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


class PortLayout(QHBoxLayout):
    _baudrate = 115200
    _timeout = 1

    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, logger):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.logger = logger
        self.serialPort = serial.Serial()

        self.label_text = "Port:"
        self.button_labels = ["Connect", "Disconnect"]

        self.label = QLabel()
        self.combo_box = QComboBox()
        self.button = QPushButton()

        self.initUI()

    @staticmethod
    def listSerialPort() -> list[ListPortInfo]:
        ports_list = []
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            ports_list.append(port)
        return ports_list

    def newSession(self):
        self.combo_box.clear()
        self.combo_box.addItems(self.listSerialPort())
        self.button.setText(self.button_labels[0])
        self.buttonState()

    def initUI(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.combo_box.addItems(self.listSerialPort())

        self.button.setText(self.button_labels[0])
        self.button.setFixedWidth(self._button_width)
        self.button.clicked.connect(self.execute)
        self.buttonState()

        self.addWidget(self.label)
        self.addWidget(self.combo_box)
        self.addWidget(self.button)

    def buttonState(self):
        if self.combo_box.currentIndex() == -1:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def execute(self):
        user_input = self.combo_box.currentText()

        if self.button.text() == self.button_labels[0]:
            self.portConnect(user_input)
            self.button.setText(self.button_labels[1])
        elif self.button.text() == self.button_labels[1]:
            self.portDisconnect(user_input)
            self.button.setText(self.button_labels[0])

    def portConnect(self, port: str) -> None:
        self.serialPort.port = port
        self.serialPort.baudrate = self._baudrate
        self.serialPort.timeout = self._timeout

        try:
            self.serialPort.open()
            self.logger.setTextColor(QColor(0, 255, 0))
            self.logger.append(f"Connected: {port}")

        except serial.SerialException as e:
            self.logger.setTextColor(QColor(255, 0, 0))
            self.logger.append(f"Failed to open serial port: {e}")

    def portDisconnect(self, port: str) -> None:
        if self.serialPort.is_open:
            self.serialPort.close()
        self.logger.setTextColor(QColor(255, 0, 0))
        self.logger.append(f"Disconnected: {port}")
