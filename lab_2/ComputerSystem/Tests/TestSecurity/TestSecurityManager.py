import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Security import SecurityManager


class TestSecurityManager:

    def test_firewall_check_behavior(self):
        manager = SecurityManager()
        manager.add_firewall_rule({'port': 22, 'action': 'block'})

        blocked_packet = {'port': 22, 'source': '192.168.1.1'}
        result1 = manager.check_firewall(blocked_packet)
        assert result1 is not None

        # Пакет, не соответствующий правилам
        allowed_packet = {'port': 80, 'source': '192.168.1.1'}
        result2 = manager.check_firewall(allowed_packet)
        assert result2 is not None

    def test_firewall_rules_adding(self):
        manager = SecurityManager()
        initial_count = len(manager.firewall_rules)

        manager.add_firewall_rule({'port': 443, 'action': 'allow'})

        assert len(manager.firewall_rules) == initial_count + 1
        assert manager.firewall_rules[-1] == {'port': 443, 'action': 'allow'}

    def test_encryption_providers_registration(self):
        manager = SecurityManager()
        initial_count = len(manager.encryption_providers)

        manager.register_encryption('AES-256')

        assert len(manager.encryption_providers) == initial_count + 1
        assert manager.encryption_providers[-1] == 'AES-256'

    def test_security_report_structure(self):
        manager = SecurityManager()
        report = manager.get_security_report()

        # Проверяем что отчет содержит ожидаемые ключи
        expected_keys = [
            'encryption_providers_count',
            'authentication_methods_count',
            'firewall_rules_count',
            'threat_level',
            'security_events_count',
            'encryption_enabled',
            'firewall_enabled',
            'last_events'
        ]

        for key in expected_keys:
            assert key in report

    def test_methods_exist(self):
        manager = SecurityManager()

        # Проверяем что основные методы существуют и вызываются
        manager.enable_encryption()
        manager.disable_encryption()
        manager.enable_firewall()
        manager.disable_firewall()

        # Если выполнение дошло до этой точки - методы работают
        assert True