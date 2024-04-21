from node_editor.gui.attributes import Node


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, data):
        super().__init__()
        self.title_text = data["name"]
        self.type_text = "Device Node"
        self.set_color(title_color=(170, 90, 10))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        self.attributes = data["attributes"]
        self.description = data["description"]

        for attribute in self.attributes:
            self.add_pin(pin_text=attribute["name"], is_output=attribute['is_output'])
