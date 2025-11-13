from typing import Dict


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