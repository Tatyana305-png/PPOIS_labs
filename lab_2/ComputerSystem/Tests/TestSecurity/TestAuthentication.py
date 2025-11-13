import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Security import AuthenticationSystem, PasswordChecker
from Exceptions.AuthenticationException import AuthenticationException


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