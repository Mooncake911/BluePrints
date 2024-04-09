from node_editor.attributes import Node


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, name="Name", pins=None):
        super().__init__()
        if pins is None:
            pins = {"is_output": [], "is_input": []}

        self.title_text = f"{name}"
        self.type_text = "Device Node"
        self.set_color(title_color=(170, 90, 10))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        for pin_name in pins["is_output"]:
            self.add_pin(pin_text=pin_name, is_output=True)
        for pin_name in pins["is_input"]:
            self.add_pin(pin_text=pin_name, is_output=False)
