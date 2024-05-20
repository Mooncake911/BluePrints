from PySide6 import QtWidgets
from node_editor.gui.attributes import Node


class Parameter_Node(Node):
    type_list = ['integer', 'float', 'boolean', 'string']
    color_list = [(0, 255, 255), (75, 0, 130), (255, 69, 0), (0, 128, 0)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.combo_box = QtWidgets.QComboBox()
        self.line_edit = QtWidgets.QLineEdit()

        self.title_text = "Parameter"
        self.type_text = "Data Types"
        self.set_color(title_color=(255, 255, 255))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)
        self.add_pin(pin_text="value", is_output=False)
        self.add_pin(pin_text="value", is_output=True)

    def line_edit_user_input(self, text):
        self.metadata["value"] = text
        self.title_text = text
        self.build()

    def combo_box_user_input(self, index):
        if index > -1:
            self.set_color(title_color=self.color_list[index])
        self.metadata["index"] = index
        self.type_text = f"{self.type_list[index].capitalize()} Types"
        self.build()

    def init_widget(self):
        # Line Edit
        value = self.metadata.get("value", "Parameter")
        self.line_edit_user_input(value)
        self.line_edit.setText(value)
        self.line_edit.textChanged.connect(self.line_edit_user_input)
        self.line_edit.setFixedWidth(100)
        self.layout.addWidget(self.line_edit)

        # Combo Box
        index = self.metadata.get("index", -1)
        self.combo_box_user_input(index)
        self.combo_box.addItems(self.type_list)
        self.combo_box.setCurrentIndex(index)
        self.combo_box.currentIndexChanged.connect(self.combo_box_user_input)
        self.combo_box.setFixedWidth(100)
        self.layout.addWidget(self.combo_box)

        super().init_widget()
