from node_editor.gui.attributes import Node
from devices import DEVICES_NAMES


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data = DEVICES_NAMES[kwargs.get("name")]

        self.metadata["id"] = data["id"]
        self.description = data["description"]

        self.title_text = data["name"]
        self.type_text = "Device Node"
        self.set_color(title_color=(170, 90, 10))

        self.add_pin(pin_text="::Ex In", is_output=False, execution=True, visible=False)
        self.add_pin(pin_text="::Ex Out", is_output=True, execution=True, visible=False)

        attributes = data["attributes"]
        for attribute in attributes:
            if attribute['show_attribute']:
                if attribute['readable']:
                    self.add_pin(pin_text=attribute["name"], is_output=attribute['readable'],
                                 pin_type=attribute["var_type"], execution=False, visible=True)
                if attribute['writable']:
                    self.add_pin(pin_text=attribute["name"], is_output=not attribute['writable'],
                                 pin_type=attribute["var_type"], execution=False, visible=True)
