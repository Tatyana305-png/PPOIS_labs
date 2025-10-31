class HardwareException(Exception):
    """Базовое исключение для аппаратных ошибок"""
    pass

class CPUOverheatException(HardwareException):
    """Исключение перегрева процессора"""
    def __init__(self, temperature):
        self.temperature = temperature
        super().__init__(f"CPU перегрет! Температура: {temperature}°C")

class MemoryAllocationException(HardwareException):
    """Исключение выделения памяти"""
    pass

class StorageFullException(HardwareException):
    """Исключение переполнения хранилища"""
    pass

class HardwareIncompatibilityException(HardwareException):
    """Исключение несовместимости оборудования"""
    pass
