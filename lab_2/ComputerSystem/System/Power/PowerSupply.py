from typing import Dict


class PowerSupply:
    def __init__(self, wattage: int, efficiency: str):
        self.wattage = wattage
        self.efficiency = efficiency
        self.is_on = False
        self.voltage_outputs = {}
        self.temperature = 25.0
        self.fan_speed = 0

    def turn_on(self):
        self.is_on = True
        self.voltage_outputs = {
            '+12V': 12.0,
            '+5V': 5.0,
            '+3.3V': 3.3
        }
        self.fan_speed = 1000

    def turn_off(self):
        self.is_on = False
        self.voltage_outputs = {}
        self.fan_speed = 0

    def get_power_consumption(self) -> Dict:
        """Получение информации о потребляемой мощности"""
        return {
            'total_wattage': self.wattage,
            'efficiency': self.efficiency,
            'outputs': self.voltage_outputs
        }