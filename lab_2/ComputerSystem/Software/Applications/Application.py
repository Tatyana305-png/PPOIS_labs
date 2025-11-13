from typing import List, Dict
from Exceptions.DependencyMissingException import DependencyMissingException

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