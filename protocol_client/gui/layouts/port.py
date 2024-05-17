from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QComboBox)
from PySide6.QtGui import QColor

from serial_port import serial_port


class PortLayout(QHBoxLayout):
    _label_width = 70
    _button_width = 100
    _layout_space = 20

    def __init__(self, text_edit):
        super().__init__()
        self.setSpacing(self._layout_space)
        serial_port.new_data.connect(self.append_data)

        self.text_edit = text_edit

        self.label_text = "Port:"
        self.button_labels = ["Connect", "Disconnect"]

        self.label = QLabel()
        self.combo_box = QComboBox()
        self.button = QPushButton()

        self.initUI()

    def append_data(self, data):
        self.text_edit.setTextColor(QColor(0, 255, 0))
        self.text_edit.append(data)

    def buttonState(self):
        if self.combo_box.currentIndex() == -1:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def initUI(self):
        self.label.setText(self.label_text)
        self.label.setFixedWidth(self._label_width)

        self.combo_box.addItems(serial_port.listSerialPort())

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
            serial_port.initSerial(port=port)
            serial_port.start()
            self.text_edit.setTextColor(QColor(0, 255, 0))
            self.text_edit.append(f"Connected to port: {serial_port.serial.port}")
        except Exception as e:
            self.text_edit.setTextColor(QColor(255, 0, 0))
            self.text_edit.append(f"Failed to open serial port: {e}")

    def portDisconnect(self) -> None:
        serial_port.close()
        self.text_edit.setTextColor(QColor(255, 0, 0))
        self.text_edit.append(f"Disconnected from port: {serial_port.serial.port}")

    def newSession(self):
        self.portDisconnect()
        self.combo_box.clear()
        self.combo_box.addItems(serial_port.listSerialPort())
        self.button.setText(self.button_labels[0])
        self.buttonState()
