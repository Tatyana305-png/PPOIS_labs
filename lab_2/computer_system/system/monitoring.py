import time
from typing import Dict, List
from datetime import datetime


class SystemMonitor:
    def __init__(self):
        self.metrics = {}
        self.alerts = []
        self.log_entries = []
        self.performance_counters = {}
        self.resource_tracker = None

    def add_metric(self, name: str, value, timestamp=None):
        """Добавление метрики"""
        if timestamp is None:
            timestamp = datetime.now()
        self.metrics[name] = {
            'value': value,
            'timestamp': timestamp
        }

    def check_alerts(self):
        """Проверка условий для алертов"""
        critical_alerts = []
        for metric_name, data in self.metrics.items():
            if 'cpu_usage' in metric_name and data['value'] > 90:
                critical_alerts.append(f"Высокая загрузка CPU: {data['value']}%")
            elif 'memory_usage' in metric_name and data['value'] > 85:
                critical_alerts.append(f"Высокая загрузка памяти: {data['value']}%")
        return critical_alerts

    def log_event(self, event: str, level: str = "INFO"):
        """Логирование события"""
        log_entry = {
            'timestamp': datetime.now(),
            'level': level,
            'event': event
        }
        self.log_entries.append(log_entry)


class PerformanceCounter:
    def __init__(self, name: str):
        self.name = name
        self.values = []
        self.timestamps = []
        self.max_samples = 1000

    def add_sample(self, value: float):
        """Добавление сэмпла производительности"""
        self.values.append(value)
        self.timestamps.append(time.time())

        # Ограничение количества хранимых сэмплов
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