from typing import Dict
from .Protocol import Protocol


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