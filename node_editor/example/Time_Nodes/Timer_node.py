from PySide6 import QtWidgets, QtCore
from node_editor.gui.attributes import Node


class Timer_Node(Node):
    _format = "hh:mm:ss:zzz"
    timers_id = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.combo_box = QtWidgets.QComboBox()
        self.time_edit = QtWidgets.QTimeEdit()

        self.title_text = "Timer"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 165, 0))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

    def timer_user_input(self, text):
        self.metadata["value"] = text.toString(self._format)

    def combo_box_user_input(self, text):
        index = text + 1
        self.metadata["index"] = index
        self.title_path.clear()
        self.title_text = f"Timer {index}"
        self.build()

    def init_widget(self):
        index = self.metadata.get("index", 1)
        self.title_text = f"Timer {index}"

        # Combo Box
        self.combo_box.addItems(self.timers_id)
        self.combo_box.setCurrentIndex(self.timers_id.index(str(index)))
        self.combo_box.currentIndexChanged.connect(self.combo_box_user_input)
        self.combo_box.setFixedWidth(100)
        self.layout.addWidget(self.combo_box)

        # Time Edit
        value = self.metadata.get("value", "00:00:00")
        self.time_edit.setTime(QtCore.QTime.fromString(value, self._format))
        self.time_edit.timeChanged.connect(self.timer_user_input)
        self.time_edit.setDisplayFormat(self._format)
        self.time_edit.setFixedWidth(100)
        self.layout.addWidget(self.time_edit)

        super().init_widget()
