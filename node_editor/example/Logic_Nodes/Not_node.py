from node_editor.gui.attributes import Node


class Not_Node(Node):
    def __init__(self, name, scene):
        super().__init__(name, scene)

        self.title_text = "NOT"
        self.type_text = "Logic Node"
        self.set_color(title_color=(128, 128, 128))

        self.add_pin(pin_text="::Ex In", is_output=False, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, visible=False)
