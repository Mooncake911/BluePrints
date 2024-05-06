from node_editor.gui.attributes import Node


class Add_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_text = "Add"
        self.type_text = "Logic Node"
        self.set_color(title_color=(0, 128, 0))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        self.add_pin(pin_text="input A", is_output=False)
        self.add_pin(pin_text="input B", is_output=False)
        self.add_pin(pin_text="output", is_output=True)
