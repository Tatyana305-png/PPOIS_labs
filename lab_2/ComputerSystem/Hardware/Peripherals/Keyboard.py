from typing import List
from .Peripheral import Peripheral


class Keyboard(Peripheral):
    def __init__(self, layout: str, backlight: bool):
        super().__init__("Keyboard", "USB")
        self.layout = layout
        self.backlight = backlight
        self.pressed_keys = []
        self.keyboard_type = "Mechanical"
        self.num_keys = 104

    def key_press(self, key: str):
        """Нажатие клавиши"""
        self.pressed_keys.append(key)
        print(f"Нажата клавиша: {key}")
        return f"Нажата клавиша: {key}"

    def key_release(self, key: str):
        """Отпускание клавиши"""
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            print(f"Отпущена клавиша: {key}")

    def get_key_combination(self) -> List[str]:
        """Получение текущей комбинации клавиш"""
        return self.pressed_keys.copy()

    def toggle_backlight(self):
        """Переключение подсветки"""
        self.backlight = not self.backlight
        status = "включена" if self.backlight else "выключена"
        print(f"Подсветка клавиатуры {status}")

    def set_backlight_brightness(self, level: int):
        """Установка яркости подсветки"""
        if 0 <= level <= 100:
            print(f"Яркость подсветки установлена на {level}%")
        else:
            print("Некорректный уровень яркости")

    def get_keyboard_info(self) -> dict:
        """Получение информации о клавиатуре"""
        base_info = self.get_info()
        base_info.update({
            'layout': self.layout,
            'backlight': self.backlight,
            'keyboard_type': self.keyboard_type,
            'num_keys': self.num_keys,
            'pressed_keys': len(self.pressed_keys)
        })
        return base_info