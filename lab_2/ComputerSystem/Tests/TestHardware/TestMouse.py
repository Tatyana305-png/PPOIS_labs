import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Peripherals.Mouse import Mouse

class TestMouse:
    def test_mouse_initialization(self):
        mouse = Mouse(1600, 6)
        assert mouse.dpi == 1600
        assert mouse.buttons == 6
        assert mouse.position == (0, 0)
        assert mouse.mouse_type == "Optical"
        assert mouse.polling_rate == 1000
        assert mouse.name == "Mouse"
        assert mouse.connection_type == "USB"

    def test_mouse_move(self):
        mouse = Mouse(1600, 6)
        position = mouse.move(100, 200)

        assert mouse.position == (100, 200)
        assert position == (100, 200)

    def test_mouse_click_valid_button(self):
        mouse = Mouse(1600, 6)
        result = mouse.click(1)

        assert result == "Нажата кнопка мыши: 1"

    def test_mouse_click_invalid_button(self):
        mouse = Mouse(1600, 6)
        result = mouse.click(0)

        assert result == "Ошибка: неверный номер кнопки"

        result = mouse.click(7)
        assert "Ошибка" in result

    def test_mouse_scroll_valid_directions(self):
        mouse = Mouse(1600, 6)

        mouse.scroll("up")
        mouse.scroll("down")

    def test_mouse_scroll_invalid_direction(self):
        mouse = Mouse(1600, 6)
        mouse.scroll("invalid")

    def test_mouse_set_dpi(self):
        mouse = Mouse(1600, 6)
        mouse.set_dpi(3200)

        assert mouse.dpi == 3200

    def test_mouse_get_mouse_info(self):
        mouse = Mouse(1600, 6)
        mouse.move(150, 300)
        mouse.set_dpi(2400)

        info = mouse.get_mouse_info()
        assert info['dpi'] == 2400
        assert info['buttons'] == 6
        assert info['position'] == (150, 300)
        assert info['mouse_type'] == "Optical"
        assert info['polling_rate'] == 1000
        assert info['name'] == "Mouse"
        assert info['connection_type'] == "USB"