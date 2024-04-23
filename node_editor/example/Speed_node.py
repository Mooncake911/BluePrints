from node_editor.gui.attributes import Node


class Speed_Node(Node):
    def __init__(self, name):
        super().__init__(name)

        self.title_text = "Speed"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 128, 0))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        self.add_pin(pin_text="Get", is_output=False)
        self.add_pin(pin_text="Return", is_output=True)
