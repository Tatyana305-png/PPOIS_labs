import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from software.os import OperatingSystem, Kernel
from software.applications import Application, TextEditor, WebBrowser, WebTab
from software.utilities import FileManager, CompressionUtility, SystemCleaner
from exceptions.software_exceptions import DependencyMissingException, VersionCompatibilityException


class TestOSAdditional:
    def test_kernel_comprehensive(self):
        kernel = Kernel()

        # Test driver registration
        drivers = ["network_driver", "storage_driver", "usb_driver"]
        for driver in drivers:
            kernel.register_driver(driver)

        assert len(kernel.drivers) == 3

        # Test interrupt handlers
        def mock_handler(data):
            return f"handled: {data}"

        kernel.interrupt_handlers[1] = mock_handler
        result = kernel.handle_interrupt(1, "test_data")
        assert result == "handled: test_data"

        # Test unknown interrupt
        result = kernel.handle_interrupt(999, "data")
        assert result is None

    def test_os_process_management(self):
        os = OperatingSystem("TestOS", "1.0")
        editor = TextEditor()

        os.install_application(editor)
        process_id = os.run_application("TextEditor")

        assert process_id in os.running_processes
        assert os.running_processes[process_id] == editor

        # Test shutdown with running processes
        os.shutdown()


class TestApplicationsAdditional:
    def test_application_dependencies(self):
        app = Application("TestApp", "1.0")

        class MockDependency:
            def __init__(self, name, available):
                self.name = name  # ДОБАВЛЕНО: атрибут name
                self.available = available

            def is_available(self):
                return self.available

        # Test with available dependencies
        app.dependencies = [
            MockDependency("lib1", True),
            MockDependency("lib2", True)
        ]
        assert app.check_dependencies() is True

        # Test with missing dependency
        app.dependencies.append(MockDependency("missing_lib", False))
        with pytest.raises(DependencyMissingException):
            app.check_dependencies()

    def test_text_editor_comprehensive(self):
        editor = TextEditor()

        # Test multiple file operations
        files = ["doc1.txt", "doc2.txt", "doc3.txt"]
        for file in files:
            editor.open_file(file)

        assert editor.current_file == "doc3.txt"
        assert len(editor.open_files) == 3

        # Test save with content
        save_result = editor.save_file("Line 1\nLine 2\nLine 3")
        assert "сохранен" in save_result

        # Test spell checker integration (mock)
        errors = editor.spell_check("This is correct text")
        assert isinstance(errors, list)  # Просто проверяем что возвращает список

    def test_web_browser_comprehensive(self):
        browser = WebBrowser()

        # Test multiple tabs
        urls = [
            "https://example.com",
            "https://google.com",
            "https://github.com"
        ]

        tabs = []
        for url in urls:
            tab = browser.open_tab(url)
            tabs.append(tab)

        assert len(browser.open_tabs) == 3
        assert browser.current_tab == tabs[-1]

        # Test tab navigation
        browser.current_tab.navigate("https://newurl.com")
        assert browser.current_tab.url == "https://newurl.com"
        # История должна содержать предыдущий URL
        assert "https://github.com" in browser.current_tab.history

        # Test tab closing
        browser.close_tab(tabs[0])
        assert len(browser.open_tabs) == 2

    def test_web_tab_comprehensive(self):
        tab = WebTab("https://start.com")

        # Test navigation history - ИСПРАВЛЕННАЯ ЧАСТЬ
        urls = [
            "https://page1.com",
            "https://page2.com",
            "https://page3.com"
        ]

        for url in urls:
            tab.navigate(url)

        assert tab.url == "https://page3.com"
        # История должна содержать: start.com, page1.com, page2.com (page3.com - текущий, не в истории)
        assert len(tab.history) == 3

        # Test back navigation
        tab.go_back()
        assert tab.url == "https://page2.com"

        tab.go_back()
        assert tab.url == "https://page1.com"


class TestUtilitiesAdditional:
    def test_file_manager_comprehensive(self):
        fm = FileManager()

        # Test directory operations
        fm.create_directory("docs")
        fm.create_directory("pictures")

        # Test file operations (mock)
        files = fm.list_files()
        assert isinstance(files, list)

        fm.delete_file("old_file.txt")

        # Test current directory
        fm.current_directory = "/home/user"
        assert fm.current_directory == "/home/user"

    def test_compression_utility(self):
        comp = CompressionUtility()

        # Test compression
        files = ["file1.txt", "file2.jpg", "file3.pdf"]
        result = comp.compress_files(files, "archive.zip")
        assert result is True

        # Test extraction
        result = comp.extract_files("archive.zip", "/tmp/extract")
        assert result is True

        # Test supported formats
        assert len(comp.supported_formats) > 0
        assert 'zip' in comp.supported_formats

    def test_system_cleaner(self):
        cleaner = SystemCleaner()

        # Test scanning
        junk_count = cleaner.scan_system()
        assert junk_count >= 0
        assert len(cleaner.temp_files) >= 0
        assert len(cleaner.cache_directories) >= 0

        # Test cleaning
        cleaned_count = cleaner.clean_system()
        assert cleaned_count == junk_count
        assert len(cleaner.temp_files) == 0
        assert len(cleaner.cache_directories) == 0