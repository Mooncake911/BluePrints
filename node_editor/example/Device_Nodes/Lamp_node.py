from node_editor.attributes import Node

counter = 0


class Lamp_Node(Node):
    def __init__(self):
        super().__init__()
        global counter
        counter += 1

        self.title_text = f"Lamp_{counter}"
        self.type_text = "Device Node"
        self.set_color(title_color=(170, 90, 10))

        self.add_pin(name="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(name="::Ex Out", is_output=True, execution=True, visible=False)

        self.add_pin(name="brightness", is_output=False)
        self.add_pin(name="mode", is_output=False)
