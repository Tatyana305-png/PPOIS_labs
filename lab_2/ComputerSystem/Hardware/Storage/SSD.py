from .StorageDevice import StorageDevice


class SSD(StorageDevice):
    def __init__(self, capacity: int, interface: str):
        super().__init__(capacity, "SSD")
        self.interface = interface
        self.write_endurance = 1000000
        self.bytes_written = 0
        self.controller = "Phison"
        self.nand_type = "TLC"

    def get_health_status(self):
        if self.used_space >= self.capacity:
            return 0
        health_percentage = 100 - (self.used_space / self.capacity) * 100
        return max(0, min(100, health_percentage))

    def trim(self):
        """Команда TRIM для оптимизации SSD"""
        print("Выполняется TRIM команда для оптимизации SSD")
        self.health_status = max(0, self.health_status - 0.001)

    def over_provision(self, percentage: int):
        """Настройка over-provisioning"""
        print(f"Over-provisioning установлен на {percentage}%")

    def get_ssd_info(self) -> dict:
        """Получение информации о SSD"""
        base_info = self.get_storage_info()
        base_info.update({
            'interface': self.interface,
            'write_endurance': self.write_endurance,
            'bytes_written': self.bytes_written,
            'controller': self.controller,
            'nand_type': self.nand_type,
            'health_status': self.get_health_status()
        })
        return base_info

    def store_file(self, filename: str, data: bytes, encryption_handler=None) -> bool:
        """Переопределение метода хранения файла для отслеживания записи"""
        result = super().store_file(filename, data, encryption_handler)
        if result:
            self.bytes_written += len(data)
        return result