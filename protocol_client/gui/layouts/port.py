from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QComboBox)
from PySide6.QtGui import QColor
from PySide6.QtCore import QThread, Signal

import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


class SerialThread(QThread):
    stop_flag = False
    exit_func = None

    new_data = Signal(str)
    encoding = 'utf-8'

    def __init__(self, port=None, baud_rate=115200, timeout=1):
        super().__init__()
        self.serial = serial.Serial()
        self.initSerial(port, baud_rate, timeout)

    def initSerial(self, port, baud_rate=115200, timeout=1, exit_func=None):
        self.stop_flag = False
        self.exit_func = exit_func
        self.serial.port = port
        self.serial.baudrate = baud_rate
        self.serial.timeout = timeout

    def run(self):
        self.serial.open()
        while not self.stop_flag:
            try:
                if self.serial.in_waiting:
                    self.read()
            except serial.serialutil.SerialException:
                self.close()
        if not self.serial.is_open:
            self.exit_func()

    def close(self):
        if self.serial.is_open:
            self.stop_flag = True
            self.serial.close()

    def write(self, data):
        if self.serial.is_open:
            self.serial.write(data.encode(self.encoding))
            self.new_data.emit(data)

    def read(self):
        if self.serial.is_open:
            data = self.serial.readline().decode(self.encoding)
            if data:
                self.new_data.emit(data)


class PortLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, text_edit):
        super().__init__()
        self.setSpacing(self._layout_space)

        self.text_edit = text_edit
        self.serialPort = SerialThread()
        self.serialPort.new_data.connect(self.append_data)

        self.label_text = "Port:"
        self.button_labels = ["Connect", "Disconnect"]

        self.label = QLabel()
        self.combo_box = QComboBox()
        self.button = QPushButton()

        self.initUI()

    def append_data(self, data):
        self.text_edit.setTextColor(QColor(0, 255, 0))
        self.text_edit.append(data)

    @staticmethod
    def listSerialPort() -> list[ListPortInfo]:
        ports_list = []
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            ports_list.append(port)
        return ports_list

    def buttonState(self):
        if self.combo_box.currentIndex() == -1:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

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

    def execute(self):
        if self.button.text() == self.button_labels[0]:
            self.portConnect()
            self.button.setText(self.button_labels[1])
        elif self.button.text() == self.button_labels[1]:
            self.portDisconnect()
            self.button.setText(self.button_labels[0])

    def portConnect(self) -> None:
        port = self.combo_box.currentText()
        try:
            self.serialPort.initSerial(port=port, exit_func=self.newSession)
            self.serialPort.start()
            self.text_edit.setTextColor(QColor(0, 255, 0))
            self.text_edit.append(f"Connected to port: {self.serialPort.serial.port}")

        except serial.SerialException as e:
            self.text_edit.setTextColor(QColor(255, 0, 0))
            self.text_edit.append(f"Failed to open serial port: {e}")

    def portDisconnect(self) -> None:
        self.serialPort.close()
        self.text_edit.setTextColor(QColor(255, 0, 0))
        self.text_edit.append(f"Disconnected from port: {self.serialPort.serial.port}")

    def newSession(self):
        self.portDisconnect()
        self.combo_box.clear()
        self.combo_box.addItems(self.listSerialPort())
        self.button.setText(self.button_labels[0])
        self.buttonState()
