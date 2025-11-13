from .HardwareException import HardwareException

class CPUOverheatException(HardwareException):
    """Исключение перегрева процессора"""
    def __init__(self, temperature):
        self.temperature = temperature
        super().__init__(f"CPU перегрет! Температура: {temperature}°C")