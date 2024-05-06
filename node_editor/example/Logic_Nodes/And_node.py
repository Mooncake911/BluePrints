from node_editor.gui.attributes import Node


class And_Node(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_text = "AND"
        self.type_text = "Logic Node"
        self.set_color(title_color=(128, 128, 128))

        self.add_pin(pin_text="::Ex In 1", is_output=False, visible=False)
        self.add_pin(pin_text="::Ex In 2", is_output=False, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, visible=False)
