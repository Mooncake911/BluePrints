from node_editor.attributes import Node


class Equal_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "=="
        self.type_text = "Arithmetic Node"
        self.set_color(title_color=(128, 128, 128))

        self.add_pin(name="::Ex In 1", is_output=False, visible=False)
        self.add_pin(name="::Ex In 2", is_output=False, visible=False)
        self.add_pin(name="::Ex Out", is_output=True, visible=False)
