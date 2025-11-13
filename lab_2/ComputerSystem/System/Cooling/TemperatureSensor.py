import random
from datetime import datetime


class TemperatureSensor:
    def __init__(self, location: str, min_temp: float = -20.0, max_temp: float = 120.0):
        self.location = location
        self.current_temp = 25.0
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.temperature_history = []
        self.calibration_offset = 0.0
        self.is_active = True
        self.last_updated = datetime.now()
        self.error_count = 0
        self.critical_threshold = 90.0
        self.warning_threshold = 70.0

    def update_temperature(self, new_temp: float):
        """Обновить температуру"""
        if not self.min_temp <= new_temp <= self.max_temp:
            self.error_count += 1
            raise ValueError(f"Температура {new_temp} вне диапазона ({self.min_temp}-{self.max_temp})")

        self.current_temp = new_temp
        self.temperature_history.append((datetime.now(), new_temp))
        self.last_updated = datetime.now()

        if len(self.temperature_history) > 1000:
            self.temperature_history.pop(0)

    def simulate_temperature_change(self, base_temp: float = 25.0, fluctuation: float = 5.0):
        """Симуляция изменения температуры (для тестирования)"""
        new_temp = base_temp + random.uniform(-fluctuation, fluctuation)
        new_temp = max(self.min_temp, min(self.max_temp, new_temp))
        self.update_temperature(new_temp)
        return new_temp

    def calibrate(self, offset: float):
        """Калибровка датчика"""
        self.calibration_offset = offset
        print(f"Датчик {self.location} откалиброван со смещением {offset}°C")

    def get_temperature_status(self) -> str:
        """Получить статус температуры"""
        temp = self.get_temperature()
        if temp >= self.critical_threshold:
            return "CRITICAL"
        elif temp >= self.warning_threshold:
            return "WARNING"
        elif temp <= 0:
            return "FREEZING"
        else:
            return "NORMAL"

    def get_trend(self, points: int = 10) -> str:
        """Определить тренд температуры"""
        if len(self.temperature_history) < points:
            return "UNKNOWN"

        recent_temps = [temp for _, temp in self.temperature_history[-points:]]
        if len(recent_temps) < 2:
            return "STABLE"

        avg_change = sum(recent_temps[i] - recent_temps[i - 1] for i in range(1, len(recent_temps))) / (
                    len(recent_temps) - 1)

        if avg_change > 0.5:
            return "RISING"
        elif avg_change < -0.5:
            return "FALLING"
        else:
            return "STABLE"

    def reset_sensor(self):
        """Сброс датчика к начальному состоянию"""
        self.current_temp = 25.0
        self.error_count = 0
        self.is_active = True
        print(f"Датчик {self.location} сброшен")

    def disable(self):
        """Отключить датчик"""
        self.is_active = False
        print(f"Датчик {self.location} отключен")

    def enable(self):
        """Включить датчик"""
        self.is_active = True
        print(f"Датчик {self.location} включен")

    def get_stats(self) -> dict:
        """Получить статистику датчика"""
        if not self.temperature_history:
            return {}

        temps = [temp for _, temp in self.temperature_history]
        return {
            'current': self.get_temperature(),
            'min': min(temps),
            'max': max(temps),
            'avg': sum(temps) / len(temps),
            'trend': self.get_trend(),
            'status': self.get_temperature_status(),
            'errors': self.error_count,
            'readings_count': len(self.temperature_history)
        }

    def set_thresholds(self, warning: float, critical: float):
        """Установить пороговые значения"""
        if warning >= critical:
            raise ValueError("Предупреждающий порог должен быть ниже критического")

        self.warning_threshold = warning
        self.critical_threshold = critical
        print(f"Пороги установлены: предупреждение при {warning}°C, критический при {critical}°C")
