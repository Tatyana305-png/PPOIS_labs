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


class Battery:
    def __init__(self, capacity: int, chemistry: str):
        self.capacity = capacity
        self.chemistry = chemistry
        self.current_charge = capacity
        self.health = 100.0
        self.cycle_count = 0
        self.charger = None

    def discharge(self, amount: int) -> bool:
        """Разрядка батареи"""
        if self.current_charge >= amount:
            self.current_charge -= amount
            self.health = max(0, self.health - 0.001)
            return True
        return False

    def charge(self, amount: int):
        """Зарядка батареи"""
        self.current_charge = min(self.capacity, self.current_charge + amount)
        self.cycle_count += 1 if self.current_charge == self.capacity else 0

    def get_battery_info(self) -> Dict:
        """Получение информации о батарее"""
        return {
            'capacity': self.capacity,
            'current_charge': self.current_charge,
            'percentage': (self.current_charge / self.capacity) * 100,
            'health': self.health,
            'cycles': self.cycle_count
        }