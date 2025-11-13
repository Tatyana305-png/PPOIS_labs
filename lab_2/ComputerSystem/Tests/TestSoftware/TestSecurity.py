import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Security import AuthenticationSystem, PasswordChecker

class TestSecurity:
    @pytest.fixture
    def sample_auth_system(self):
        return AuthenticationSystem()

    @pytest.fixture
    def sample_password_checker(self):
        return PasswordChecker()

    def test_register_user_success(self, sample_auth_system, sample_password_checker):
        sample_auth_system.register_user("user1", "StrongPass123!", sample_password_checker)
        assert "user1" in sample_auth_system.users

    def test_authenticate_success(self, sample_auth_system, sample_password_checker):
        sample_auth_system.register_user("user1", "StrongPass123!", sample_password_checker)
        result = sample_auth_system.authenticate("user1", "StrongPass123!")
        assert result is True

    def test_password_checker(self, sample_password_checker):
        assert sample_password_checker.is_strong_password("StrongPass123!") is True
        assert sample_password_checker.is_strong_password("123") is False