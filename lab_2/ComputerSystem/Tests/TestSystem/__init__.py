"""
Тесты системных компонентов
===========================

Модули:
- TestPower.py - тесты питания и батареи
- TestCooling.py - тесты системы охлаждения
- TestMonitoring.py - тесты мониторинга системы
"""

__all__ = [
    'TestPower',
    'TestCooling',
    'TestMonitoring'
]

from .TestPower import TestPower
from .TestCooling import TestCooling
from .TestMonitoring import TestMonitoring