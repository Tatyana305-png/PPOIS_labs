from .StorageDevice import StorageDevice


class HardDrive(StorageDevice):
    def __init__(self, capacity: int, rpm: int):
        super().__init__(capacity, "HDD")
        self.rpm = rpm
        self.sectors = {}
        self.heads = 2
        self.cylinders = 1000
        self.seek_time = 8.5

    def defragment(self):
        """Дефрагментация жесткого диска"""
        print(f"Дефрагментация HDD {self.rpm}RPM...")
        self.health_status = max(0, self.health_status - 0.01)

    def read_sector(self, sector: int) -> bytes:
        """Чтение сектора"""
        if sector in self.sectors:
            return self.sectors[sector]
        return b'\x00' * 512

    def write_sector(self, sector: int, data: bytes):
        """Запись сектора"""
        self.sectors[sector] = data
        print(f"Сектор {sector} записан")

    def get_hdd_info(self) -> dict:
        """Получение информации о HDD"""
        base_info = self.get_storage_info()
        base_info.update({
            'rpm': self.rpm,
            'sectors_count': len(self.sectors),
            'heads': self.heads,
            'cylinders': self.cylinders,
            'seek_time': self.seek_time
        })
        return base_info

    def spin_up(self):
        """Раскрутка диска"""
        print(f"HDD раскручивается до {self.rpm} RPM")

    def spin_down(self):
        """Остановка диска"""
        print("HDD останавливается")