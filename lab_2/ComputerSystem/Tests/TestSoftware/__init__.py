"""
Тесты программного обеспечения
==============================

Модули:
- TestOperationSystem.py - тесты операционной системы и ядра
- TestApplications.py - тесты приложений
- TestSecurity.py - тесты системы безопасности
- TestUtilities.py - тесты утилит
"""

__all__ = [
    'TestOperatingSystem',
    'TestApplications',
    'TestSecurity',
    'TestUtilities'
]

from .TestOperatingSystem import TestOperatingSystem
from .TestApplications import TestApplications
from .TestSecurity import TestSecurity
from .TestUtilities import TestUtilities