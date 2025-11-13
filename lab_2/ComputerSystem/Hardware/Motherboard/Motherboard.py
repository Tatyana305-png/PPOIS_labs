from Hardware.CPU.CPU import CPU
from Hardware.Memory.RAM import RAM

class Motherboard:
    def __init__(self, model: str, chipset: str):
        self.model = model
        self.chipset = chipset
        self.cpu_socket = None
        self.ram_slots = []
        self.connected_devices = {}
        self.bios_version = "1.0"
        self.south_bridge = None
        self.north_bridge = None
        self.pci_slots = []
        self.sata_ports = []
        self.usb_ports = []

    def install_cpu(self, cpu: CPU):
        """Установка процессора на материнскую плату"""
        if self.cpu_socket is not None:
            print("Сокет CPU уже занят")
            return

        self.cpu_socket = cpu
        print(f"Установлен процессор {cpu.brand} {cpu.model}")

    def install_ram(self, ram: RAM, slot: int):
        """Установка оперативной памяти"""
        if slot < len(self.ram_slots):
            self.ram_slots[slot] = ram
        else:
            self.ram_slots.append(ram)
        print(f"RAM установлена в слот {slot}")

    def connect_device(self, device, port: str):
        """Подключение устройства к материнской плате"""
        self.connected_devices[port] = device
        print(f"Устройство подключено к порту {port}")

    def disconnect_device(self, port: str):
        """Отключение устройства"""
        if port in self.connected_devices:
            del self.connected_devices[port]
            print(f"Устройство отключено от порта {port}")
        else:
            print(f"Порт {port} не занят")

    def get_total_ram(self):
        total = 0
        for ram_module in self.ram_slots:
            if ram_module is not None:
                # Попробуйте разные возможные атрибуты
                if hasattr(ram_module, 'total_capacity'):
                    total += ram_module.total_capacity
                elif hasattr(ram_module, 'capacity'):
                    total += ram_module.capacity
                elif hasattr(ram_module, 'size'):
                    total += ram_module.size
                elif hasattr(ram_module, 'memory_size'):
                    total += ram_module.memory_size
        return total

    def get_motherboard_info(self) -> dict:
        """Получение информации о материнской плате"""
        return {
            'model': self.model,
            'chipset': self.chipset,
            'bios_version': self.bios_version,
            'cpu_installed': self.cpu_socket is not None,
            'ram_slots_used': len([ram for ram in self.ram_slots if ram]),
            'total_ram': self.get_total_ram(),
            'connected_devices': len(self.connected_devices),
            'pci_slots': len(self.pci_slots),
            'sata_ports': len(self.sata_ports),
            'usb_ports': len(self.usb_ports)
        }

    def add_pci_slot(self, slot_type: str):
        """Добавление PCI слота"""
        self.pci_slots.append(slot_type)
        print(f"Добавлен PCI слот типа {slot_type}")

    def add_sata_port(self):
        """Добавление SATA порта"""
        self.sata_ports.append(f"SATA_{len(self.sata_ports)}")
        print(f"Добавлен SATA порт")

    def add_usb_port(self, version: str):
        """Добавление USB порта"""
        self.usb_ports.append(version)
        print(f"Добавлен USB порт {version}")

    def power_on(self):
        """Включение питания материнской платы"""
        print(f"Материнская плата {self.model} включена")

    def power_off(self):
        """Выключение питания материнской платы"""
        print(f"Материнская плата {self.model} выключена")