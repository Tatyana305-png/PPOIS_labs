import time
from typing import List


class PerformanceCounter:
    def __init__(self, name: str):
        self.name = name
        self.values: List[float] = []
        self.timestamps: List[float] = []
        self.max_samples = 1000

    def add_sample(self, value: float):
        """Добавление сэмпла производительности"""
        self.values.append(value)
        self.timestamps.append(time.time())

        if len(self.values) > self.max_samples:
            self.values.pop(0)
            self.timestamps.pop(0)

    def get_average(self, window: int = 10) -> float:
        """Получение среднего значения за окно"""
        samples = self.values[-window:]
        return sum(samples) / len(samples) if samples else 0

    def get_max(self, window: int = 10) -> float:
        """Получение максимального значения за окно"""
        samples = self.values[-window:]
        return max(samples) if samples else 0