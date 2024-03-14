from node_editor.attributes import Node


class Speed_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Speed"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 128, 0))

        self.add_pin(name="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(name="::Ex Out", is_output=True, execution=True, visible=False)

        self.add_pin(name="Get", is_output=False)
        self.add_pin(name="Return", is_output=True)
