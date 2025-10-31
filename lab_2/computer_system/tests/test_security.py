import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from software.security import AuthenticationSystem, PasswordChecker, EncryptionProvider
from exceptions.security_exceptions import AuthenticationException, EncryptionException


class TestAuthentication:
    @pytest.fixture
    def sample_auth_system(self):
        return AuthenticationSystem()

    @pytest.fixture
    def sample_password_checker(self):
        return PasswordChecker()

    def test_auth_system_initialization(self, sample_auth_system):
        assert sample_auth_system.users == {}
        assert sample_auth_system.failed_attempts == {}
        assert sample_auth_system.max_attempts == 3

    def test_register_user_success(self, sample_auth_system, sample_password_checker):
        sample_auth_system.register_user("user1", "StrongPass123!", sample_password_checker)
        assert "user1" in sample_auth_system.users
        assert 'hashed_password' in sample_auth_system.users["user1"]
        assert 'salt' in sample_auth_system.users["user1"]

    def test_register_user_weak_password(self, sample_auth_system, sample_password_checker):
        with pytest.raises(AuthenticationException):
            sample_auth_system.register_user("user1", "123", sample_password_checker)

    def test_authenticate_success(self, sample_auth_system, sample_password_checker):
        sample_auth_system.register_user("user1", "StrongPass123!", sample_password_checker)
        result = sample_auth_system.authenticate("user1", "StrongPass123!")
        assert result is True
        assert sample_auth_system.failed_attempts.get("user1", 0) == 0

    def test_authenticate_wrong_password(self, sample_auth_system, sample_password_checker):
        sample_auth_system.register_user("user1", "StrongPass123!", sample_password_checker)
        result = sample_auth_system.authenticate("user1", "WrongPassword")
        assert result is False
        assert sample_auth_system.failed_attempts["user1"] == 1

    def test_authenticate_user_not_found(self, sample_auth_system):
        with pytest.raises(AuthenticationException):
            sample_auth_system.authenticate("nonexistent", "password")


class TestPasswordChecker:
    @pytest.fixture
    def sample_password_checker(self):
        return PasswordChecker()

    def test_password_checker_initialization(self, sample_password_checker):
        assert sample_password_checker.min_length == 8
        assert sample_password_checker.require_uppercase is True
        assert sample_password_checker.require_lowercase is True
        assert sample_password_checker.require_numbers is True
        assert sample_password_checker.require_special is True

    def test_strong_password(self, sample_password_checker):
        assert sample_password_checker.is_strong_password("StrongPass123!") is True

    def test_weak_passwords(self, sample_password_checker):
        assert sample_password_checker.is_strong_password("short") is False  # Too short
        assert sample_password_checker.is_strong_password("nouppercase123!") is False  # No uppercase
        assert sample_password_checker.is_strong_password("NOLOWERCASE123!") is False  # No lowercase
        assert sample_password_checker.is_strong_password("NoNumbers!") is False  # No numbers
        assert sample_password_checker.is_strong_password("NoSpecial123") is False  # No special


class TestEncryption:
    @pytest.fixture
    def sample_encryption_provider(self):
        return EncryptionProvider("AES-256")

    @pytest.fixture
    def mock_key_manager(self):
        class MockKeyManager:
            def get_key(self):
                return b"test_key_1234567890123456"  # 32 bytes for AES-256

        return MockKeyManager()

    def test_encryption_provider_initialization(self, sample_encryption_provider):
        assert sample_encryption_provider.algorithm == "AES-256"

    def test_encryption_decryption(self, sample_encryption_provider, mock_key_manager):
        original_data = b"Secret message for encryption"

        encrypted = sample_encryption_provider.encrypt(original_data, mock_key_manager)
        decrypted = sample_encryption_provider.decrypt(encrypted, mock_key_manager)

        assert encrypted != original_data
        assert decrypted == original_data

    def test_encryption_with_invalid_key_manager(self, sample_encryption_provider):
        class InvalidKeyManager:
            def get_key(self):
                raise Exception("Key error")

        with pytest.raises(EncryptionException):
            sample_encryption_provider.encrypt(b"data", InvalidKeyManager())