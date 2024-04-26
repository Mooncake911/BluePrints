from node_editor.gui.attributes import Node
from devices import DEVICES_NAMES


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, name, scene):
        super().__init__(name, scene)
        data = DEVICES_NAMES[name]

        self.title_text = data["name"]
        self.type_text = "Device Node"
        self.set_color(title_color=(170, 90, 10))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        self.attributes = data["attributes"]
        self.description = data["description"]

        for attribute in self.attributes:
            if attribute['show_attribute']:
                if attribute['has_output']:
                    self.add_pin(pin_text=attribute["name"], is_output=attribute['has_output'])
                if attribute['has_input']:
                    self.add_pin(pin_text=attribute["name"], is_output=not attribute['has_input'])
