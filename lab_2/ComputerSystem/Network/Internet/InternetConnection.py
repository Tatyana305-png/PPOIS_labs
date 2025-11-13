from typing import Dict


class InternetConnection:
    def __init__(self, connection_type: str, speed: int):
        self.connection_type = connection_type
        self.speed = speed
        self.is_connected = False
        self.ip_address = None
        self.dns_servers = []
        self.router = None

    def connect(self):
        self.is_connected = True
        self.ip_address = "192.168.1.100"
        return "Подключение к интернету установлено"

    def disconnect(self):
        self.is_connected = False
        self.ip_address = None
        return "Отключено от интернета"

    def measure_latency(self) -> int:
        """Измерение задержки соединения"""
        if not self.is_connected:
            return -1

        import random
        self.latency = random.randint(10, 100)
        return self.latency

    def get_connection_status(self) -> Dict:
        return {
            'connected': self.is_connected,
            'type': self.connection_type,
            'speed': self.speed,
            'ip': self.ip_address
        }