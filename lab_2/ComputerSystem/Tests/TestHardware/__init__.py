"""
Тесты аппаратного обеспечения
=============================

Модули:
- TestCPU.py - тесты процессора и ядер
- TestMemory.py - тесты оперативной памяти и модулей
- TestStorage.py - тесты устройств хранения данных
- TestMotherboard.py - тесты материнской платы и BIOS
- TestPeripherals.py - тесты периферийных устройств
- TestKeyboard.py - тесты клавиатуры
- TestMonitor.py - тесты монитора
- TestMouse.py - тесты мыши
"""

__all__ = [
    'TestCPU',
    'TestMemory',
    'TestStorage',
    'TestMotherboard',
    'TestPeripherals',
    'TestKeyboard',
    'TestMonitor',
    'TestMouse',
    'TestRAM',
    'TestBIOS',
    'TestPeripheralInheritance'
]

from .TestCPU import TestCPU
from .TestMemory import TestMemory
from .TestStorage import TestStorage
from .TestMotherboard import TestMotherboard
from .TestPeripherals import TestPeripherals
from .TestKeyboard import TestKeyboard
from .TestMonitor import TestMonitor
from .TestMouse import TestMouse
from .TestRAM import TestRAM
from .TestBIOS import TestBIOS
from .TestPeripheralInheritance import TestPeripheralInheritance