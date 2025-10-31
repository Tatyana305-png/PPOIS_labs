from typing import Dict, List


class Protocol:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.headers = {}
        self.port = 0

    def create_packet(self, data: bytes) -> bytes:
        """Создание пакета"""
        header = f"{self.name}/{self.version}".encode()
        return header + b"\r\n\r\n" + data

    def parse_packet(self, packet: bytes) -> bytes:
        """Парсинг пакета"""
        # Простой парсинг - возвращаем данные после заголовков
        parts = packet.split(b"\r\n\r\n", 1)
        return parts[1] if len(parts) > 1 else b""


class HTTPProtocol(Protocol):
    def __init__(self):
        super().__init__("HTTP", "1.1")
        self.port = 80
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']

    def create_request(self, method: str, path: str, headers: Dict, body: str = "") -> str:
        """Создание HTTP запроса"""
        request = f"{method} {path} HTTP/{self.version}\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        request += f"Content-Length: {len(body)}\r\n\r\n{body}"
        return request


class TCPProtocol:
    def __init__(self):
        self.connections = {}
        self.window_size = 65535
        self.sequence_number = 0

    def establish_connection(self, host: str, port: int) -> int:
        """Установка TCP соединения"""
        connection_id = hash(f"{host}:{port}")
        self.connections[connection_id] = {
            'host': host,
            'port': port,
            'state': 'ESTABLISHED'
        }
        return connection_id

    def send_data(self, connection_id: int, data: bytes) -> bool:
        """Отправка данных через TCP"""
        if connection_id in self.connections:
            # Имитация отправки
            return True
        return False

    def close_connection(self, connection_id: int):
        """Закрытие TCP соединения"""
        if connection_id in self.connections:
            del self.connections[connection_id]