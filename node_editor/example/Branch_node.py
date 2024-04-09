from node_editor.attributes import Node


class Branch_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Branch"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 0, 128))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="True", is_output=True, execution=True)
        self.add_pin(pin_text="False", is_output=True, execution=True)
        self.add_pin(pin_text="Condition", is_output=False)
