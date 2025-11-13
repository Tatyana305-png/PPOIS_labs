from typing import List, Dict
from .Fan import Fan
from .TemperatureSensor import TemperatureSensor


class CoolingSystem:
    def __init__(self):
        self.fans: List[Fan] = []
        self.heat_sinks = []
        self.liquid_cooling = None
        self.temperature_sensors: List[TemperatureSensor] = []

    def add_fan(self, fan: Fan):
        self.fans.append(fan)

    def monitor_temperatures(self) -> Dict:
        """Мониторинг температур"""
        temps = {}
        for sensor in self.temperature_sensors:
            temps[sensor.location] = sensor.get_temperature()
        return temps

    def adjust_cooling(self, target_temp: float):
        """Регулировка системы охлаждения"""
        for fan in self.fans:
            fan.adjust_speed(target_temp)