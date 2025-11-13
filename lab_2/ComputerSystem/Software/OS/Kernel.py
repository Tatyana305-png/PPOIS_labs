class Kernel:
    def __init__(self):
        self.system_calls = {}
        self.drivers = []
        self.interrupt_handlers = {}

    def register_driver(self, driver):
        self.drivers.append(driver)

    def handle_interrupt(self, interrupt_type: int, data):
        if interrupt_type in self.interrupt_handlers:
            return self.interrupt_handlers[interrupt_type](data)
        return None