from node_editor.node import Node


class Branch_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Branch"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 0, 128))

        self.add_pin(name="::Ex In", is_output=False, execution=True)
        self.add_pin(name="True", is_output=True, execution=True)
        self.add_pin(name="False", is_output=True, execution=True)
        self.add_pin(name="Condition", is_output=False)
