import hashlib
import secrets
from Exceptions.AuthenticationException import AuthenticationException

class AuthenticationSystem:
    def __init__(self):
        self.users = {}
        self.failed_attempts = {}
        self.max_attempts = 3
        self.password_validator = None

    def register_user(self, username: str, password: str, password_checker):
        """Регистрация пользователя с проверкой пароля"""
        if not password_checker.is_strong_password(password):
            raise AuthenticationException("Слабый пароль")

        salt = secrets.token_hex(16)
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        self.users[username] = {
            'hashed_password': hashed_password,
            'salt': salt,
            'locked': False
        }

    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация пользователя"""
        if username not in self.users:
            raise AuthenticationException("Пользователь не найден")

        if self.users[username]['locked']:
            raise AuthenticationException("Учетная запись заблокирована")

        salt = self.users[username]['salt']
        hashed_attempt = hashlib.sha256((password + salt).encode()).hexdigest()

        if hashed_attempt == self.users[username]['hashed_password']:
            self.failed_attempts[username] = 0
            return True
        else:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            if self.failed_attempts[username] >= self.max_attempts:
                self.users[username]['locked'] = True
                raise AuthenticationException("Учетная запись заблокирована из-за множества неудачных попыток")
            return False