import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Peripherals import Peripheral, Keyboard, Monitor, Mouse

class TestPeripherals:
    @pytest.fixture
    def sample_keyboard(self):
        return Keyboard("QWERTY", False)

    @pytest.fixture
    def sample_mouse(self):
        return Mouse(1600, 3)

    def test_keyboard_initialization(self, sample_keyboard):
        assert sample_keyboard.name == "Keyboard"
        assert sample_keyboard.connection_type == "USB"
        assert sample_keyboard.layout == "QWERTY"

    def test_keyboard_key_press(self, sample_keyboard):
        result = sample_keyboard.key_press("A")
        assert "Нажата клавиша: A" in result
        assert "A" in sample_keyboard.pressed_keys

    def test_mouse_move(self, sample_mouse):
        position = sample_mouse.move(100, 200)
        assert position == (100, 200)
        assert sample_mouse.position == (100, 200)

    def test_peripheral_base_class(self):
        peripheral = Peripheral("Scanner", "USB")
        assert peripheral.name == "Scanner"
        assert peripheral.connection_type == "USB"
        assert not peripheral.is_connected

        peripheral.connect()
        assert peripheral.is_connected

        peripheral.disconnect()
        assert not peripheral.is_connected

    def test_keyboard_comprehensive(self):
        keyboard = Keyboard("AZERTY", True)

        # Test multiple key presses
        keys = ["A", "B", "Ctrl", "S"]
        for key in keys:
            keyboard.key_press(key)

        assert len(keyboard.pressed_keys) == 4
        assert keyboard.get_key_combination() == keys

        # Test backlight
        assert keyboard.backlight is True

    def test_mouse_comprehensive(self):
        mouse = Mouse(3200, 6)

        # Test multiple movements
        positions = [(100, 200), (150, 250), (200, 300)]
        for pos in positions:
            mouse.move(pos[0], pos[1])

        assert mouse.position == (200, 300)

        # Test all buttons
        for button in range(1, mouse.buttons + 1):
            result = mouse.click(button)
            assert f"кнопка мыши: {button}" in result

    def test_monitor_comprehensive(self):
        monitor = Monitor((2560, 1440), 144)

        # Test resolution changes
        resolutions = [(1920, 1080), (1280, 720), (3840, 2160)]
        for res in resolutions:
            monitor.set_resolution(res[0], res[1])
            assert monitor.current_resolution == res

        # Test brightness adjustments
        for brightness in [0, 25, 50, 75, 100, 150, -10]:
            monitor.adjust_brightness(brightness)
            assert 0 <= monitor.brightness <= 100