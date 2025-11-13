import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Peripherals.Keyboard import Keyboard
from Hardware.Peripherals.Mouse import Mouse
from Hardware.Peripherals.Peripheral import Peripheral

class TestPeripheralInheritance:
    def test_peripheral_inheritance_keyboard(self):
        keyboard = Keyboard("QWERTY-RU", True)
        assert isinstance(keyboard, Peripheral)

        info = keyboard.get_info()
        assert 'name' in info
        assert 'connection_type' in info

    def test_peripheral_inheritance_mouse(self):
        mouse = Mouse(1600, 6)
        assert isinstance(mouse, Peripheral)

        info = mouse.get_info()
        assert 'name' in info
        assert 'connection_type' in info