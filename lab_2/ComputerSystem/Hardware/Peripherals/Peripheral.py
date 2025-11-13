class Peripheral:
    def __init__(self, name: str, connection_type: str):
        self.name = name
        self.connection_type = connection_type
        self.is_connected = False
        self.driver = None
        self.manufacturer = "Unknown"
        self.model = "Standard"

    def connect(self):
        """Подключение периферийного устройства"""
        self.is_connected = True
        print(f"{self.name} подключен через {self.connection_type}")

    def disconnect(self):
        """Отключение периферийного устройства"""
        self.is_connected = False
        print(f"{self.name} отключен")

    def install_driver(self, driver_name: str):
        """Установка драйвера"""
        self.driver = driver_name
        print(f"Драйвер '{driver_name}' установлен для {self.name}")

    def get_info(self) -> dict:
        """Получение информации об устройстве"""
        return {
            'name': self.name,
            'connection_type': self.connection_type,
            'is_connected': self.is_connected,
            'driver': self.driver,
            'manufacturer': self.manufacturer,
            'model': self.model
        }

    def test_device(self) -> bool:
        """Тестирование устройства"""
        print(f"Тестирование {self.name}...")
        return self.is_connected