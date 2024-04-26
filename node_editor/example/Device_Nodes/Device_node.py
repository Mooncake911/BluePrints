from node_editor.gui.attributes import Node
from devices import DEVICES_NAMES


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, name):
        super().__init__(name)
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
                if attribute['readable']:
                    self.add_pin(pin_text=attribute["readable"], is_output=attribute['readable'])
                if attribute['writable']:
                    self.add_pin(pin_text=attribute["writable"], is_output=not attribute['writable'])
