from typing import List

class BluetoothAdapter:
    def __init__(self, version: str):
        self.version = version
        self.is_enabled = False
        self.paired_devices = []
        self.connected_devices = []

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False
        self.connected_devices = []

    def pair_device(self, device_name: str, address: str) -> bool:
        """Сопряжение устройства"""
        device = {'name': device_name, 'address': address, 'paired': True}
        self.paired_devices.append(device)
        return True

    def connect_device(self, address: str) -> bool:
        """Подключение устройства"""
        for device in self.paired_devices:
            if device['address'] == address:
                self.connected_devices.append(device)
                return True
        return False