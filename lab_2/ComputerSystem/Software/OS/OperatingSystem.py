from Exceptions.ApplicationCrashException import ApplicationCrashException

class OperatingSystem:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.kernel = None
        self.process_manager = None
        self.memory_manager = None
        self.file_system = None
        self.running_processes = {}
        self.installed_applications = []
        self.system_settings = {}
        self.user_sessions = []
        self.security_module = None

    def boot(self):
        """Загрузка операционной системы"""
        print(f"Загружается {self.name} версии {self.version}")

    def shutdown(self):
        """Выключение операционной системы"""
        print("Выключение операционной системы...")

    def install_application(self, application):
        """Установка приложения"""
        self.installed_applications.append(application)

    def run_application(self, app_name: str):
        """Запуск приложения"""
        for app in self.installed_applications:
            if app.name == app_name:
                process_id = f"process_{len(self.running_processes)}"
                self.running_processes[process_id] = app
                return process_id
        raise ApplicationCrashException(f"Приложение {app_name} не найдено")