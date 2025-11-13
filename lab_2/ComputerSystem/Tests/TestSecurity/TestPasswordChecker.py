import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Security import PasswordChecker

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
        assert sample_password_checker.is_strong_password("short") is False
        assert sample_password_checker.is_strong_password("nouppercase123!") is False
        assert sample_password_checker.is_strong_password("NOLOWERCASE123!") is False
        assert sample_password_checker.is_strong_password("NoNumbers!") is False
        assert sample_password_checker.is_strong_password("NoSpecial123") is False