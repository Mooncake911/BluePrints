from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Timer_Event_Node(Node):
    counter = 0
    timers_id = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.combo_box = QtWidgets.QComboBox()

        Timer_Event_Node.counter += 1
        self.title_text = f"Timer Event {self.index}"
        self.type_text = "Timer Nodes"
        self.set_color(title_color=(255, 165, 0))

        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

    def combo_box_user_input(self, text):
        self.index = text + 1
        self.title_path.clear()
        self.title_text = f"Timer Event {self.index}"
        self.build()

    def init_widget(self):
        if not self.index:
            self.index = self.counter
        self.title_text = f"Timer Event {self.index}"

        # Combo Box
        self.combo_box.addItems(self.timers_id)
        self.combo_box.setCurrentIndex(self.index - 1)
        self.combo_box.currentIndexChanged.connect(self.combo_box_user_input)
        self.combo_box.setFixedWidth(100)
        self.layout.addWidget(self.combo_box)

        super().init_widget()
