import json
from node_editor.gui.attributes import Node
from node_editor.constants import get_device_name


class Device_Node(Node):
    """
    A node that describes any device.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        DEVICES_NAMES = get_device_name()
        data = DEVICES_NAMES[kwargs.get("name")]

        if data.get("id"):
            self.metadata["id"] = data["id"]
        if data.get("open_key"):
            self.metadata["open_key"] = data["open_key"]

        self.description = json.dumps(data, indent=4, ensure_ascii=False)

        self.title_text = data.get("name")
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
