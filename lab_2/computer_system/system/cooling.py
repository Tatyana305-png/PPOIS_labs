from typing import List, Dict


class CoolingSystem:
    def __init__(self):
        self.fans = []
        self.heat_sinks = []
        self.liquid_cooling = None
        self.temperature_sensors = []

    def add_fan(self, fan):
        self.fans.append(fan)

    def monitor_temperatures(self) -> Dict:  # Теперь Dict определен
        """Мониторинг температур"""
        temps = {}
        for sensor in self.temperature_sensors:
            temps[sensor.location] = sensor.get_temperature()
        return temps

    def adjust_cooling(self, target_temp: float):
        """Регулировка системы охлаждения"""
        for fan in self.fans:
            fan.adjust_speed(target_temp)


class Fan:
    def __init__(self, size: int, max_rpm: int):
        self.size = size
        self.max_rpm = max_rpm
        self.current_rpm = 0
        self.location = "unknown"

    def set_speed(self, rpm: int):
        self.current_rpm = min(rpm, self.max_rpm)

    def adjust_speed(self, target_temp: float):
        """Автоматическая регулировка скорости на основе температуры"""
        if target_temp > 80:
            self.set_speed(self.max_rpm)
        elif target_temp > 60:
            self.set_speed(self.max_rpm * 0.7)
        else:
            self.set_speed(self.max_rpm * 0.4)


class TemperatureSensor:
    def __init__(self, location: str):
        self.location = location
        self.current_temp = 25.0

    def get_temperature(self) -> float:
        return self.current_temp

    def update_temperature(self, new_temp: float):
        self.current_temp = new_temp