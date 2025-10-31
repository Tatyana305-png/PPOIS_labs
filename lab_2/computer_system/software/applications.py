import datetime
from typing import List, Dict
from exceptions.software_exceptions import DependencyMissingException


class Application:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.dependencies = []
        self.configuration = {}
        self.is_running = False
        self.window_manager = None
        self.resource_manager = None

    def start(self):
        """Запуск приложения"""
        self.is_running = True
        return f"Приложение {self.name} запущено"

    def stop(self):
        """Остановка приложения"""
        self.is_running = False
        return f"Приложение {self.name} остановлено"

    def check_dependencies(self) -> bool:
        """Проверка зависимостей"""
        for dependency in self.dependencies:
            if not dependency.is_available():
                raise DependencyMissingException(f"Отсутствует зависимость: {dependency.name}")
        return True


class TextEditor(Application):
    def __init__(self):
        super().__init__("TextEditor", "1.0")
        self.open_files = []
        self.current_file = None
        self.spell_checker = None

    def open_file(self, filename: str):
        self.current_file = filename
        self.open_files.append(filename)
        return f"Открыт файл: {filename}"

    def save_file(self, content: str):
        if self.current_file:
            return f"Файл {self.current_file} сохранен"
        return "Нет открытого файла для сохранения"

    def spell_check(self, text: str) -> List[str]:
        if self.spell_checker:
            return self.spell_checker.check(text)
        return []


class WebBrowser(Application):
    def __init__(self):
        super().__init__("WebBrowser", "2.0")
        self.open_tabs = []
        self.current_tab = None
        self.download_manager = None
        self.cookie_manager = None

    def open_tab(self, url: str):
        tab = WebTab(url)
        self.open_tabs.append(tab)
        self.current_tab = tab
        return tab

    def close_tab(self, tab):
        if tab in self.open_tabs:
            self.open_tabs.remove(tab)
            if self.current_tab == tab:
                self.current_tab = self.open_tabs[0] if self.open_tabs else None


class WebTab:
    def __init__(self, url: str):
        self.url = url
        self.history = []
        self.cookies = {}
        self.load_time = datetime.datetime.now()

    def navigate(self, new_url: str):
        self.history.append(self.url)
        self.url = new_url

    def go_back(self):
        if self.history:
            self.url = self.history.pop()