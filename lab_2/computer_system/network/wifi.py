from typing import List, Dict


class WiFiAdapter:
    def __init__(self, standard: str, frequency: str):
        self.standard = standard
        self.frequency = frequency
        self.is_enabled = False
        self.connected_network = None
        self.available_networks = []
        self.signal_strength = 0

    def enable(self):
        self.is_enabled = True
        self.scan_networks()

    def disable(self):
        self.is_enabled = False
        self.connected_network = None
        self.available_networks = []

    def scan_networks(self) -> List[Dict]:
        """Сканирование доступных сетей"""
        self.available_networks = [
            {'ssid': 'HomeWiFi', 'signal': 85, 'security': 'WPA2'},
            {'ssid': 'Office', 'signal': 70, 'security': 'WPA3'},
            {'ssid': 'FreeWiFi', 'signal': 60, 'security': 'Open'}
        ]
        return self.available_networks

    def connect(self, ssid: str, password: str = None) -> bool:
        """Подключение к WiFi сети"""
        for network in self.available_networks:
            if network['ssid'] == ssid:
                self.connected_network = network
                self.signal_strength = network['signal']
                return True
        return False

    def get_connection_info(self) -> Dict:
        if self.connected_network:
            return {
                'ssid': self.connected_network['ssid'],
                'signal': self.signal_strength,
                'security': self.connected_network['security']
            }
        return {}


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