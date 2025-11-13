import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Peripherals.Keyboard import Keyboard

class TestKeyboard:
    def test_keyboard_initialization(self):
        keyboard = Keyboard("QWERTY-RU", True)
        assert keyboard.layout == "QWERTY-RU"
        assert keyboard.backlight == True
        assert keyboard.pressed_keys == []
        assert keyboard.keyboard_type == "Mechanical"
        assert keyboard.num_keys == 104
        assert keyboard.name == "Keyboard"
        assert keyboard.connection_type == "USB"

    def test_keyboard_key_press(self):
        keyboard = Keyboard("QWERTY-RU", True)
        result = keyboard.key_press("A")

        assert "A" in keyboard.pressed_keys
        assert result == "Нажата клавиша: A"

    def test_keyboard_key_release(self):
        keyboard = Keyboard("QWERTY-RU", True)
        keyboard.key_press("A")
        keyboard.key_press("B")

        keyboard.key_release("A")
        assert "A" not in keyboard.pressed_keys
        assert "B" in keyboard.pressed_keys

    def test_keyboard_get_key_combination(self):
        keyboard = Keyboard("QWERTY-RU", True)
        keyboard.key_press("Ctrl")
        keyboard.key_press("C")

        combination = keyboard.get_key_combination()
        assert "Ctrl" in combination
        assert "C" in combination
        assert len(combination) == 2

        # Проверяем что возвращается копия, а не оригинал
        combination.append("Extra")
        assert "Extra" not in keyboard.pressed_keys

    def test_keyboard_toggle_backlight(self):
        keyboard = Keyboard("QWERTY-RU", True)
        initial_state = keyboard.backlight

        keyboard.toggle_backlight()
        assert keyboard.backlight != initial_state

        keyboard.toggle_backlight()
        assert keyboard.backlight == initial_state

    def test_keyboard_set_backlight_brightness(self):
        keyboard = Keyboard("QWERTY-RU", True)

        keyboard.set_backlight_brightness(75)

        keyboard.set_backlight_brightness(150)

    def test_keyboard_get_keyboard_info(self):
        keyboard = Keyboard("QWERTY-RU", True)
        keyboard.key_press("A")
        keyboard.key_press("B")

        info = keyboard.get_keyboard_info()
        assert info['layout'] == "QWERTY-RU"
        assert info['backlight'] == True
        assert info['keyboard_type'] == "Mechanical"
        assert info['num_keys'] == 104
        assert info['pressed_keys'] == 2
        assert info['name'] == "Keyboard"
        assert info['connection_type'] == "USB"