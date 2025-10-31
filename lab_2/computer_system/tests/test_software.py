import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from software.os import OperatingSystem, Kernel
from software.applications import TextEditor, WebBrowser, WebTab
from software.security import AuthenticationSystem, PasswordChecker, EncryptionProvider
from software.utilities import FileManager
from exceptions.software_exceptions import ApplicationCrashException
from exceptions.security_exceptions import AuthenticationException, EncryptionException


class TestOperatingSystem:
    @pytest.fixture
    def sample_os(self):
        return OperatingSystem("Linux", "5.0")

    def test_os_initialization(self, sample_os):
        assert sample_os.name == "Linux"
        assert sample_os.version == "5.0"
        assert sample_os.running_processes == {}

    def test_install_application(self, sample_os):
        editor = TextEditor()
        sample_os.install_application(editor)
        assert len(sample_os.installed_applications) == 1


class TestApplications:
    @pytest.fixture
    def sample_text_editor(self):
        return TextEditor()

    def test_application_start_stop(self, sample_text_editor):
        start_result = sample_text_editor.start()
        assert "запущено" in start_result
        assert sample_text_editor.is_running

        stop_result = sample_text_editor.stop()
        assert "остановлено" in stop_result
        assert not sample_text_editor.is_running

    def test_text_editor_file_operations(self, sample_text_editor):
        sample_text_editor.open_file("test.txt")
        assert sample_text_editor.current_file == "test.txt"


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


class TestUtilities:
    @pytest.fixture
    def sample_file_manager(self):
        return FileManager()

    def test_file_manager_initialization(self, sample_file_manager):
        assert sample_file_manager.current_directory == "/"

    def test_file_manager_list_files(self, sample_file_manager):
        files = sample_file_manager.list_files()
        assert isinstance(files, list)