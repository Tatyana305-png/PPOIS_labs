import hashlib
import secrets
from typing import Optional
from exceptions.security_exceptions import AuthenticationException, EncryptionException


class SecurityManager:
    def __init__(self):
        self.encryption_providers = []
        self.authentication_methods = {}
        self.firewall_rules = []
        self.antivirus_scanner = None
        self.intrusion_detection = None

    def register_encryption(self, provider):
        self.encryption_providers.append(provider)

    def add_firewall_rule(self, rule):
        self.firewall_rules.append(rule)


class EncryptionProvider:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.key_storage = None

    def encrypt(self, data: bytes, key_manager) -> bytes:
        """Шифрование данных"""
        try:
            key = key_manager.get_key()
            # Простая имитация шифрования XOR
            encrypted = bytes(b ^ 0xAA for b in data)
            return encrypted
        except Exception as e:
            raise EncryptionException(f"Ошибка шифрования: {str(e)}")

    def decrypt(self, encrypted_data: bytes, key_manager) -> bytes:
        """Дешифрование данных"""
        try:
            key = key_manager.get_key()
            # Дешифрование XOR
            decrypted = bytes(b ^ 0xAA for b in encrypted_data)
            return decrypted
        except Exception as e:
            raise EncryptionException(f"Ошибка дешифрования: {str(e)}")


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


class PasswordChecker:
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special = True

    def is_strong_password(self, password: str) -> bool:
        """Проверка сложности пароля"""
        if len(password) < self.min_length:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if self.require_uppercase and not has_upper:
            return False
        if self.require_lowercase and not has_lower:
            return False
        if self.require_numbers and not has_digit:
            return False
        if self.require_special and not has_special:
            return False

        return True