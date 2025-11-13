class SecurityManager:
    def __init__(self):
        self.encryption_providers = []
        self.authentication_methods = {}
        self.firewall_rules = []
        self.antivirus_scanner = None
        self.intrusion_detection = None
        self.firewall_enabled = True
        self.encryption_enabled = False
        self.threat_level = 'low'
        self.security_log = []

    def register_encryption(self, provider):
        self.encryption_providers.append(provider)
        print(f"Провайдер шифрования зарегистрирован: {provider}")

    def add_firewall_rule(self, rule):
        self.firewall_rules.append(rule)
        print(f"Правило фаервола добавлено: {rule}")

    def _matches_rule(self, packet: dict, rule: dict) -> bool:
        """Проверяет, соответствует ли пакет правилу"""
        for key, value in rule.items():
            if key != 'action' and key in packet and packet[key] != value:
                return False
        return True

    def log_security_event(self, event: str):
        """Логирование событий безопасности"""
        self.security_log.append(event)
        print(f"Событие безопасности: {event}")

    def check_firewall(self, packet: dict) -> bool:
        """Проверка пакета через фаервол"""
        if not self.firewall_enabled:
            return True

        for rule in self.firewall_rules:
            if self._matches_rule(packet, rule):
                self.log_security_event(f"Пакет заблокирован правилом: {rule}")
                return False

        return True

    def get_security_report(self) -> dict:
        """Получение отчета о безопасности"""
        return {
            'encryption_providers_count': len(self.encryption_providers),
            'authentication_methods_count': len(self.authentication_methods),
            'firewall_rules_count': len(self.firewall_rules),
            'threat_level': self.threat_level,
            'security_events_count': len(self.security_log),
            'encryption_enabled': self.encryption_enabled,
            'firewall_enabled': self.firewall_enabled,
            'last_events': self.security_log[-5:] if self.security_log else []
        }

    def enable_encryption(self):
        """Включение шифрования"""
        self.encryption_enabled = True
        self.log_security_event("Шифрование включено")

    def disable_encryption(self):
        """Отключение шифрования"""
        self.encryption_enabled = False
        self.log_security_event("Шифрование отключено")

    def enable_firewall(self):
        """Включение фаервола"""
        self.firewall_enabled = True
        self.log_security_event("Фаервол включен")

    def disable_firewall(self):
        """Отключение фаервола"""
        self.firewall_enabled = False
        self.log_security_event("Фаервол отключен")