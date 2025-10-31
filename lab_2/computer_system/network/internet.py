from typing import List, Dict
import urllib.parse


class InternetConnection:
    def __init__(self, connection_type: str, speed: int):
        self.connection_type = connection_type
        self.speed = speed
        self.is_connected = False
        self.ip_address = None
        self.dns_servers = []
        self.router = None

    def connect(self):
        self.is_connected = True
        self.ip_address = "192.168.1.100"
        return "Подключение к интернету установлено"

    def disconnect(self):
        self.is_connected = False
        self.ip_address = None
        return "Отключено от интернета"

    def get_connection_status(self) -> Dict:
        return {
            'connected': self.is_connected,
            'type': self.connection_type,
            'speed': self.speed,
            'ip': self.ip_address
        }


class WebClient:
    def __init__(self):
        self.cookies = {}
        self.user_agent = "WebClient/1.0"
        self.download_manager = None
        self.cache_manager = None

    def get_request(self, url: str) -> str:
        """GET запрос"""
        parsed_url = urllib.parse.urlparse(url)
        return f"GET {parsed_url.path} HTTP/1.1\nHost: {parsed_url.netloc}\nUser-Agent: {self.user_agent}"

    def post_request(self, url: str, data: Dict) -> str:
        """POST запрос"""
        parsed_url = urllib.parse.urlparse(url)
        post_data = "&".join([f"{k}={v}" for k, v in data.items()])
        return f"POST {parsed_url.path} HTTP/1.1\nHost: {parsed_url.netloc}\nContent-Type: application/x-www-form-urlencoded\n\n{post_data}"


class EmailClient:
    def __init__(self):
        self.smtp_server = None
        self.pop3_server = None
        self.messages = []
        self.contacts = []

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Отправка email"""
        message = {
            'to': to,
            'subject': subject,
            'body': body,
            'sent': True
        }
        self.messages.append(message)
        return True

    def receive_emails(self) -> List[Dict]:
        """Получение email"""
        # Имитация получения писем
        new_emails = [
            {'from': 'sender@example.com', 'subject': 'Test', 'body': 'Hello'}
        ]
        self.messages.extend(new_emails)
        return new_emails