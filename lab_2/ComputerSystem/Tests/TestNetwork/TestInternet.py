import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Network.Internet import InternetConnection, WebClient, EmailClient

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