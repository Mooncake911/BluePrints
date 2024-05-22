from node_editor.gui.attributes import Node


class Dimming_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_text = "Dimming"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 0, 128))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)
        self.add_pin(pin_text="bool", is_output=False)
        self.add_pin(pin_text="int", is_output=True)

