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
        parts = packet.split(b"\r\n\r\n", 1)
        return parts[1] if len(parts) > 1 else b""