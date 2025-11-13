import hashlib
from Exceptions.StorageFullException import StorageFullException


class StorageDevice:
    def __init__(self, capacity: int, type: str):
        self.capacity = capacity
        self.type = type
        self.used_space = 0
        self.files = {}
        self.encryption_key = None
        self.serial_number = "SN000001"
        self.health_status = 100.0

    def store_file(self, filename: str, data: bytes, encryption_handler=None) -> bool:
        """Хранение файла с возможным шифрованием"""
        if self.used_space + len(data) > self.capacity:
            raise StorageFullException("Недостаточно места на устройстве")

        if encryption_handler:
            data = encryption_handler.encrypt(data)

        self.files[filename] = data
        self.used_space += len(data)
        self.health_status = max(0, self.health_status - 0.0001)
        print(f"Файл '{filename}' сохранен ({len(data)} байт)")
        return True

    def read_file(self, filename: str, decryption_handler=None) -> bytes:
        """Чтение файла с возможным дешифрованием"""
        if filename not in self.files:
            raise FileNotFoundError(f"Файл {filename} не найден")

        data = self.files[filename]
        if decryption_handler:
            data = decryption_handler.decrypt(data)

        print(f"Файл '{filename}' прочитан ({len(data)} байт)")
        return data

    def delete_file(self, filename: str):
        """Удаление файла"""
        if filename in self.files:
            file_size = len(self.files[filename])
            del self.files[filename]
            self.used_space -= file_size
            print(f"Файл '{filename}' удален")
        else:
            print(f"Файл '{filename}' не найден")

    def calculate_hash(self, filename: str) -> str:
        """Вычисление хеша файла"""
        if filename not in self.files:
            raise FileNotFoundError(f"Файл {filename} не найден")
        file_hash = hashlib.sha256(self.files[filename]).hexdigest()
        print(f"Хеш файла '{filename}': {file_hash}")
        return file_hash

    def get_storage_info(self) -> dict:
        """Получение информации о хранилище"""
        return {
            'capacity': self.capacity,
            'used_space': self.used_space,
            'free_space': self.capacity - self.used_space,
            'type': self.type,
            'files_count': len(self.files),
            'health_status': self.health_status,
            'utilization': (self.used_space / self.capacity) * 100
        }

    def format(self):
        """Форматирование устройства"""
        self.files.clear()
        self.used_space = 0
        print(f"Устройство {self.type} отформатировано")