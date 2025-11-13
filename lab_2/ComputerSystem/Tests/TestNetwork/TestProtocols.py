import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Network.Protocols import Protocol, HTTPProtocol, TCPProtocol

class TestProtocols:
    def test_protocol_base_class(self):
        protocol = Protocol("FTP", "2.0")
        protocol.port = 21

        assert protocol.name == "FTP"
        assert protocol.version == "2.0"
        assert protocol.port == 21

        test_data = b"test data"
        packet = protocol.create_packet(test_data)
        parsed_data = protocol.parse_packet(packet)
        assert parsed_data == test_data

    def test_http_protocol_comprehensive(self):
        http = HTTPProtocol()

        assert http.port == 80
        assert 'GET' in http.methods
        assert 'POST' in http.methods

        headers = {
            "User-Agent": "TestClient/1.0",
            "Accept": "application/json"
        }
        request = http.create_request("GET", "/api/data", headers)

        assert "GET /api/data HTTP/1.1" in request
        assert "User-Agent: TestClient/1.0" in request
        assert "Accept: application/json" in request

        request_with_body = http.create_request(
            "POST",
            "/api/users",
            headers,
            '{"name": "John"}'  # Длина 15 символов
        )
        assert "Content-Length: 16" in request_with_body
        assert '{"name": "John"}' in request_with_body

    def test_tcp_protocol_comprehensive(self):
        tcp = TCPProtocol()

        conn1 = tcp.establish_connection("192.168.1.100", 8080)
        conn2 = tcp.establish_connection("10.0.0.5", 443)

        assert conn1 in tcp.connections
        assert conn2 in tcp.connections
        assert tcp.connections[conn1]['state'] == 'ESTABLISHED'

        result1 = tcp.send_data(conn1, b"Hello Server")
        result2 = tcp.send_data(999999, b"Invalid connection")  # Non-existent

        assert result1 is True
        assert result2 is False

        tcp.close_connection(conn1)
        assert conn1 not in tcp.connections
        assert conn2 in tcp.connections