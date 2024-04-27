from .pin_graphics import PinGraphics


class Pin(PinGraphics):
    def __init__(self, parent, name: str, is_output: bool, execution: bool, visible: bool = True,
                 pin_type: str = ''):
        super().__init__(parent, name, pin_type, is_output, execution, visible)

    def clear_connection(self):
        if self.connection:
            self.connection.delete()

    def can_connect_to(self, pin):
        if not pin:
            return False
        if pin.node == self.node:
            return False
        if pin.pin_type != self.pin_type and pin.pin_type != '' and self.pin_type != '':
            return False
        return pin.is_output != self.is_output and pin.execution == self.execution
