from typing import List


class Peripheral:
    def __init__(self, name: str, connection_type: str):
        self.name = name
        self.connection_type = connection_type
        self.is_connected = False
        self.driver = None

    def connect(self):
        self.is_connected = True

    def disconnect(self):
        self.is_connected = False


class Keyboard(Peripheral):
    def __init__(self, layout: str, backlight: bool):
        super().__init__("Keyboard", "USB")
        self.layout = layout
        self.backlight = backlight
        self.pressed_keys = []

    def key_press(self, key: str):
        self.pressed_keys.append(key)
        return f"Нажата клавиша: {key}"

    def get_key_combination(self) -> List[str]:
        return self.pressed_keys.copy()


class Mouse(Peripheral):
    def __init__(self, dpi: int, buttons: int):
        super().__init__("Mouse", "USB")
        self.dpi = dpi
        self.buttons = buttons
        self.position = (0, 0)

    def move(self, x: int, y: int):
        self.position = (x, y)
        return self.position

    def click(self, button: int):
        return f"Нажата кнопка мыши: {button}"


class Monitor:
    def __init__(self, resolution: tuple, refresh_rate: int):
        self.resolution = resolution
        self.refresh_rate = refresh_rate
        self.current_resolution = resolution
        self.brightness = 50
        self.graphics_card = None

    def set_resolution(self, width: int, height: int):
        self.current_resolution = (width, height)

    def adjust_brightness(self, level: int):
        self.brightness = max(0, min(100, level))