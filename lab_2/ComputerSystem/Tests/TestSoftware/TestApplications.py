import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Applications import Application, TextEditor, WebBrowser, WebTab
from Exceptions.DependencyMissingException import DependencyMissingException

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