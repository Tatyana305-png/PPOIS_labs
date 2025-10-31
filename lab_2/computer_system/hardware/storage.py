import hashlib
from exceptions.hardware_exceptions import StorageFullException


class StorageDevice:
    def __init__(self, capacity: int, type: str):
        self.capacity = capacity
        self.type = type
        self.used_space = 0
        self.files = {}
        self.encryption_key = None

    def store_file(self, filename: str, data: bytes, encryption_handler=None) -> bool:
        """Хранение файла с возможным шифрованием"""
        if self.used_space + len(data) > self.capacity:
            raise StorageFullException("Недостаточно места на устройстве")

        if encryption_handler:
            data = encryption_handler.encrypt(data)

        self.files[filename] = data
        self.used_space += len(data)
        return True

    def read_file(self, filename: str, decryption_handler=None) -> bytes:
        """Чтение файла с возможным дешифрованием"""
        if filename not in self.files:
            raise FileNotFoundError(f"Файл {filename} не найден")

        data = self.files[filename]
        if decryption_handler:
            data = decryption_handler.decrypt(data)

        return data

    def calculate_hash(self, filename: str) -> str:
        """Вычисление хеша файла"""
        if filename not in self.files:
            raise FileNotFoundError(f"Файл {filename} не найден")
        return hashlib.sha256(self.files[filename]).hexdigest()


class HardDrive(StorageDevice):
    def __init__(self, capacity: int, rpm: int):
        super().__init__(capacity, "HDD")
        self.rpm = rpm
        self.sectors = {}

    def defragment(self):
        """Дефрагментация жесткого диска"""
        # Логика дефрагментации
        pass


class SSD(StorageDevice):
    def __init__(self, capacity: int, interface: str):
        super().__init__(capacity, "SSD")
        self.interface = interface
        self.write_endurance = 1000000

    def get_health_status(self) -> float:
        """Получение статуса здоровья SSD"""
        return (self.write_endurance - self.used_space / 1000) / self.write_endurance * 100