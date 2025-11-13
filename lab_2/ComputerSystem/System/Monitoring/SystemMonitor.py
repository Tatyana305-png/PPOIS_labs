from typing import Dict, List
from datetime import datetime
from .PerformanceCounter import PerformanceCounter


class SystemMonitor:
    def __init__(self):
        self.metrics = {}
        self.alerts = []
        self.log_entries = []
        self.performance_counters: Dict[str, PerformanceCounter] = {}
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