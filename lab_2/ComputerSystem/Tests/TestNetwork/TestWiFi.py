import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Network.WiFi import WiFiAdapter, BluetoothAdapter

class TestWiFi:
    @pytest.fixture
    def sample_wifi_adapter(self):
        return WiFiAdapter("Wi-Fi 5", "2.4GHz")

    def test_wifi_adapter_initialization(self, sample_wifi_adapter):
        assert sample_wifi_adapter.standard == "Wi-Fi 5"
        assert not sample_wifi_adapter.is_enabled

    def test_bluetooth_comprehensive(self):
        bluetooth = BluetoothAdapter("5.1")

        # Test enable/disable
        bluetooth.enable()
        assert bluetooth.is_enabled is True

        bluetooth.disable()
        assert bluetooth.is_enabled is False
        assert len(bluetooth.connected_devices) == 0

        # Test device management
        bluetooth.enable()
        devices = [
            ("Headphones", "00:11:22:33:44:55"),
            ("Keyboard", "66:77:88:99:AA:BB"),
            ("Mouse", "CC:DD:EE:FF:00:11")
        ]

        for name, address in devices:
            bluetooth.pair_device(name, address)

        assert len(bluetooth.paired_devices) == 3

        # Test connection
        bluetooth.connect_device("00:11:22:33:44:55")
        assert len(bluetooth.connected_devices) == 1

        # Test connecting to non-paired device
        result = bluetooth.connect_device("non:existent:address")
        assert result is False