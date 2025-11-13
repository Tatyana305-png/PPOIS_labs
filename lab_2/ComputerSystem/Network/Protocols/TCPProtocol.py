
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
            return True
        return False

    def close_connection(self, connection_id: int):
        """Закрытие TCP соединения"""
        if connection_id in self.connections:
            del self.connections[connection_id]