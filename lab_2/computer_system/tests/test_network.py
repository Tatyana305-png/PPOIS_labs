import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network.internet import InternetConnection, WebClient
from network.wifi import WiFiAdapter

class TestInternet:
    @pytest.fixture
    def sample_internet_connection(self):
        return InternetConnection("Ethernet", 100)

    @pytest.fixture
    def sample_web_client(self):
        return WebClient()

    def test_internet_connection_initialization(self, sample_internet_connection):
        assert sample_internet_connection.connection_type == "Ethernet"
        assert not sample_internet_connection.is_connected

    def test_web_client_initialization(self, sample_web_client):
        assert sample_web_client.user_agent == "WebClient/1.0"

class TestWiFi:
    @pytest.fixture
    def sample_wifi_adapter(self):
        return WiFiAdapter("Wi-Fi 5", "2.4GHz")

    def test_wifi_adapter_initialization(self, sample_wifi_adapter):
        assert sample_wifi_adapter.standard == "Wi-Fi 5"
        assert not sample_wifi_adapter.is_enabled