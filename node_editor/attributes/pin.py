from .pin_graphics import PinGraphics


class Pin(PinGraphics):
    def __init__(self, parent, name: str, is_output: bool, execution: bool, visible: bool = True):
        super().__init__(parent, name, is_output, execution, visible)

    def clear_connection(self):
        if self.connection:
            self.connection.delete()

    def can_connect_to(self, pin):
        if not pin:
            return False
        if pin.node == self.node:
            return False
        return self.is_output != pin.is_output and pin.execution == self.execution
