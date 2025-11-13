from Exceptions.CPUOverheatException import CPUOverheatException

class CPU:
    def __init__(self, brand: str, model: str, cores: int, speed: float):
        self.brand = brand
        self.model = model
        self.cores = cores
        self.speed = speed
        self.temperature = 35.0
        self.usage = 0.0
        self.cache_memory = None
        self.thermal_threshold = 85.0
        self.cores_list = []

    def execute_instruction(self, instruction: str) -> str:
        """Выполнение инструкции процессором"""
        self.usage += 0.1
        self.temperature += 0.5
        if self.temperature > self.thermal_threshold:
            raise CPUOverheatException(self.temperature)
        return f"Выполнена инструкция: {instruction}"

    def get_temperature(self) -> float:
        """Получение текущей температуры процессора"""
        return self.temperature

    def cool_down(self):
        """Охлаждение процессора"""
        self.temperature = max(35.0, self.temperature - 10.0)
        print(f"Процессор охлажден до {self.temperature}°C")

    def get_info(self) -> dict:
        """Получение информации о процессоре"""
        return {
            'brand': self.brand,
            'model': self.model,
            'cores': self.cores,
            'speed': self.speed,
            'temperature': self.temperature,
            'usage': self.usage
        }

    def add_core(self, core):
        """Добавление ядра процессора"""
        self.cores_list.append(core)

    def get_total_power(self) -> float:
        """Расчет общей мощности процессора"""
        return self.cores * self.speed * 0.8