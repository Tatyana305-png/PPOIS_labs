import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network.internet import InternetConnection, WebClient, EmailClient
from network.wifi import WiFiAdapter, BluetoothAdapter
from network.protocols import Protocol, HTTPProtocol, TCPProtocol


class TestInternetAdditional:
    def test_email_client_comprehensive(self):
        email = EmailClient()

        # Test sending email
        result = email.send_email(
            "recipient@example.com",
            "Test Subject",
            "This is a test email body"
        )
        assert result is True
        assert len(email.messages) == 1

        # Test receiving emails
        new_emails = email.receive_emails()
        assert len(new_emails) == 1
        assert len(email.messages) == 2

        # Test message structure
        message = email.messages[0]
        assert message['to'] == "recipient@example.com"
        assert message['subject'] == "Test Subject"
        assert message['sent'] is True

    def test_web_client_comprehensive(self):
        client = WebClient()

        # Test cookies
        client.cookies["session"] = "abc123"
        client.cookies["user"] = "john_doe"
        assert len(client.cookies) == 2

        # Test different requests
        get_request = client.get_request("https://api.example.com/data")
        assert "GET" in get_request
        assert "api.example.com" in get_request

        post_data = {"username": "test", "password": "secret"}
        post_request = client.post_request("https://api.example.com/login", post_data)
        assert "POST" in post_request
        assert "username=test" in post_request


class TestWiFiAdditional:
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


class TestProtocolsAdditional:
    def test_protocol_base_class(self):
        protocol = Protocol("FTP", "2.0")
        protocol.port = 21

        assert protocol.name == "FTP"
        assert protocol.version == "2.0"
        assert protocol.port == 21

        # Test packet creation and parsing
        test_data = b"test data"
        packet = protocol.create_packet(test_data)
        parsed_data = protocol.parse_packet(packet)
        assert parsed_data == test_data

    def test_http_protocol_comprehensive(self):
        http = HTTPProtocol()

        assert http.port == 80
        assert 'GET' in http.methods
        assert 'POST' in http.methods

        # Test request creation
        headers = {
            "User-Agent": "TestClient/1.0",
            "Accept": "application/json"
        }
        request = http.create_request("GET", "/api/data", headers)

        assert "GET /api/data HTTP/1.1" in request
        assert "User-Agent: TestClient/1.0" in request
        assert "Accept: application/json" in request

        # Test request with body - ИСПРАВЛЕННАЯ ЧАСТЬ
        request_with_body = http.create_request(
            "POST",
            "/api/users",
            headers,
            '{"name": "John"}'  # Длина 15 символов
        )
        # Используем правильную длину (16 символов, включая кавычки)
        assert "Content-Length: 16" in request_with_body
        assert '{"name": "John"}' in request_with_body

    def test_tcp_protocol_comprehensive(self):
        tcp = TCPProtocol()

        # Test connection management
        conn1 = tcp.establish_connection("192.168.1.100", 8080)
        conn2 = tcp.establish_connection("10.0.0.5", 443)

        assert conn1 in tcp.connections
        assert conn2 in tcp.connections
        assert tcp.connections[conn1]['state'] == 'ESTABLISHED'

        # Test data sending
        result1 = tcp.send_data(conn1, b"Hello Server")
        result2 = tcp.send_data(999999, b"Invalid connection")  # Non-existent

        assert result1 is True
        assert result2 is False

        # Test connection closing
        tcp.close_connection(conn1)
        assert conn1 not in tcp.connections
        assert conn2 in tcp.connections