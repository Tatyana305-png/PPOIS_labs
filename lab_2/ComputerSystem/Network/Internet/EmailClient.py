from typing import List, Dict


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
        new_emails = [
            {'from': 'sender@example.com', 'subject': 'Test', 'body': 'Hello'}
        ]
        self.messages.extend(new_emails)
        return new_emails