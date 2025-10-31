from typing import List, Dict
from hardware.cpu import CPU
from hardware.memory import RAM


class Motherboard:
    def __init__(self, model: str, chipset: str):
        self.model = model
        self.chipset = chipset
        self.cpu_socket = None
        self.ram_slots: List[RAM] = []
        self.connected_devices = {}
        self.bios_version = "1.0"
        self.south_bridge = None
        self.north_bridge = None

    def install_cpu(self, cpu: CPU):
        """Установка процессора на материнскую плату"""
        self.cpu_socket = cpu
        print(f"Установлен процессор {cpu.brand} {cpu.model}")

    def install_ram(self, ram: RAM, slot: int):
        """Установка оперативной памяти"""
        if slot < len(self.ram_slots):
            self.ram_slots[slot] = ram
        else:
            self.ram_slots.append(ram)

    def connect_device(self, device, port: str):
        """Подключение устройства к материнской плате"""
        self.connected_devices[port] = device

    def get_total_ram(self) -> int:
        return sum(ram.total_capacity for ram in self.ram_slots if ram)


class BIOS:
    def __init__(self, version: str):
        self.version = version
        self.settings = {}
        self.boot_order = []

    def update_setting(self, key: str, value):
        self.settings[key] = value

    def set_boot_order(self, order: List[str]):
        self.boot_order = order

    def perform_post(self) -> bool:
        """Power-On Self-Test"""
        # Логика тестирования оборудования
        return True