from typing import List, Dict
from exceptions.hardware_exceptions import CPUOverheatException


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

    def execute_instruction(self, instruction: str) -> str:
        """Выполнение инструкции процессором"""
        self.usage += 0.1
        self.temperature += 0.5
        if self.temperature > self.thermal_threshold:
            raise CPUOverheatException(self.temperature)
        return f"Выполнена инструкция: {instruction}"

    def get_temperature(self) -> float:
        return self.temperature

    def cool_down(self):
        """Охлаждение процессора"""
        self.temperature = max(35.0, self.temperature - 10.0)


class CPUCore:
    def __init__(self, core_id: int, speed: float):
        self.core_id = core_id
        self.speed = speed
        self.current_task = None
        self.is_active = False

    def assign_task(self, task):
        self.current_task = task
        self.is_active = True

    def release_task(self):
        self.current_task = None
        self.is_active = False