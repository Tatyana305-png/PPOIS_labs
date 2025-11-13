from .Peripheral import Peripheral


class Mouse(Peripheral):
    def __init__(self, dpi: int, buttons: int):
        super().__init__("Mouse", "USB")
        self.dpi = dpi
        self.buttons = buttons
        self.position = (0, 0)
        self.mouse_type = "Optical"
        self.polling_rate = 1000  # Hz

    def move(self, x: int, y: int):
        """Перемещение мыши"""
        self.position = (x, y)
        print(f"Мышь перемещена в позицию ({x}, {y})")
        return self.position

    def click(self, button: int):
        """Нажатие кнопки мыши"""
        if 1 <= button <= self.buttons:
            print(f"Нажата кнопка мыши: {button}")
            return f"Нажата кнопка мыши: {button}"
        else:
            print("Неверный номер кнопки")
            return "Ошибка: неверный номер кнопки"

    def scroll(self, direction: str):
        """Прокрутка колесика"""
        directions = {"up": "вверх", "down": "вниз"}
        if direction in directions:
            print(f"Прокрутка {directions[direction]}")
        else:
            print("Неверное направление прокрутки")

    def set_dpi(self, new_dpi: int):
        """Установка DPI"""
        self.dpi = new_dpi
        print(f"DPI установлен на {new_dpi}")

    def get_mouse_info(self) -> dict:
        """Получение информации о мыши"""
        base_info = self.get_info()
        base_info.update({
            'dpi': self.dpi,
            'buttons': self.buttons,
            'position': self.position,
            'mouse_type': self.mouse_type,
            'polling_rate': self.polling_rate
        })
        return base_info