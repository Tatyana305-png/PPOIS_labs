from hardware.cpu import CPU
from hardware.memory import RAM, MemoryModule
from hardware.storage import SSD
from hardware.motherboard import Motherboard, BIOS
from hardware.peripherals import Keyboard, Mouse, Monitor
from software.os import OperatingSystem, Kernel
from software.applications import TextEditor, WebBrowser
from software.security import SecurityManager, AuthenticationSystem, PasswordChecker, EncryptionProvider
from software.utilities import FileManager
from network.internet import InternetConnection, WebClient
from network.wifi import WiFiAdapter
from system.power import PowerSupply, Battery
from system.cooling import CoolingSystem, Fan
from system.monitoring import SystemMonitor, PerformanceCounter
from exceptions.hardware_exceptions import CPUOverheatException
from exceptions.security_exceptions import AuthenticationException


class ComputerSystem:
    def __init__(self):
        # Инициализация компонентов
        self.cpu = CPU("Intel", "Core i9", 8, 3.6)

        # Создаем и настраиваем оперативную память с модулями
        self.ram = RAM(16384)
        memory_module = MemoryModule(8192, 3200, "DDR4")  # Создаем модуль памяти
        self.ram.add_module(memory_module)  # Добавляем модуль в RAM

        self.storage = SSD(1000000, "NVMe")
        self.motherboard = Motherboard("ASUS ROG", "Z790")
        self.bios = BIOS("2.1")

        # Периферия
        self.keyboard = Keyboard("QWERTY", True)
        self.mouse = Mouse(1600, 5)
        self.monitor = Monitor((1920, 1080), 144)

        # Программное обеспечение
        self.os = OperatingSystem("Windows", "11")
        self.kernel = Kernel()

        # Безопасность
        self.security_manager = SecurityManager()
        self.auth_system = AuthenticationSystem()
        self.password_checker = PasswordChecker()
        self.encryption_provider = EncryptionProvider("AES-256")

        # Сеть
        self.internet = InternetConnection("Fiber", 1000)
        self.wifi = WiFiAdapter("Wi-Fi 6", "5GHz")
        self.web_client = WebClient()

        # Системные компоненты
        self.power_supply = PowerSupply(850, "80+ Gold")
        self.battery = Battery(90000, "Li-ion")
        self.cooling_system = CoolingSystem()
        self.monitor_system = SystemMonitor()

        # Приложения
        self.text_editor = TextEditor()
        self.web_browser = WebBrowser()
        self.file_manager = FileManager()

        # Настройка ассоциаций
        self._setup_associations()

    def _setup_associations(self):
        """Настройка ассоциаций между компонентами"""
        # Ассоциация 1: Материнская плата содержит процессор
        self.motherboard.install_cpu(self.cpu)

        # Ассоциация 2: Материнская плата содержит оперативную память
        self.motherboard.install_ram(self.ram, 0)

        # Ассоциация 3: ОС содержит менеджер безопасности
        self.os.security_module = self.security_manager

        # Ассоциация 4: Менеджер безопасности содержит систему аутентификации
        self.security_manager.authentication_methods['password'] = self.auth_system

        # Ассоциация 5: Система аутентификации содержит проверщик паролей
        self.auth_system.password_validator = self.password_checker

        # Ассоциация 6: Менеджер безопасности содержит провайдер шифрования
        self.security_manager.encryption_providers.append(self.encryption_provider)

        # Ассоциация 7: ОС содержит приложения
        self.os.install_application(self.text_editor)
        self.os.install_application(self.web_browser)

        # Ассоциация 8: Веб-браузер содержит менеджер загрузок
        self.web_browser.download_manager = self.file_manager

        # Ассоциация 9: Система охлаждения содержит вентиляторы
        cpu_fan = Fan(120, 2000)
        self.cooling_system.add_fan(cpu_fan)

        # Ассоциация 10: Монитор системы содержит счетчики производительности
        cpu_counter = PerformanceCounter("cpu_usage")
        self.monitor_system.performance_counters['cpu'] = cpu_counter

        # Ассоциация 11: Текстовый редактор содержит проверщик орфографии
        # (имитация - в реальной системе это был бы отдельный объект)

        # Ассоциация 12: Батарея содержит зарядное устройство
        # (имитация связи)

    def demonstrate_functionality(self):
        """Демонстрация функциональности системы"""
        print("=== Демонстрация компьютерной системы ===\n")

        # Демонстрация аппаратных возможностей
        try:
            instruction_result = self.cpu.execute_instruction("ADD R1, R2")
            print(f"1. Выполнение инструкции CPU: {instruction_result}")
        except CPUOverheatException as e:
            print(f"Ошибка CPU: {e}")

        # Демонстрация работы памяти (с проверкой наличия модулей)
        if self.ram.modules:
            memory_address = self.ram.modules[0].allocate_memory(1024, "test_process")
            print(f"2. Выделено памяти по адресу: {memory_address}")
        else:
            print("2. Нет модулей памяти для выделения")

        # Демонстрация шифрования
        test_data = b"Secret data"
        try:
            encrypted = self.encryption_provider.encrypt(test_data, self)
            print(f"3. Данные зашифрованы: {len(encrypted)} байт")

            # Показать разницу между исходными и зашифрованными данными
            print(f"   Исходные данные: {test_data}")
            print(f"   Зашифрованные данные: {encrypted}")
        except Exception as e:
            print(f"3. Ошибка шифрования: {e}")

        # Демонстрация проверки пароля
        is_strong = self.password_checker.is_strong_password("StrongPass123!")
        print(f"4. Проверка сложности пароля 'StrongPass123!': {'Прошел' if is_strong else 'Не прошел'}")

        # Проверим слабый пароль для сравнения
        is_weak_strong = self.password_checker.is_strong_password("123")
        print(f"   Проверка слабого пароля '123': {'Прошел' if is_weak_strong else 'Не прошел'}")

        # Демонстрация аутентификации
        try:
            self.auth_system.register_user("admin", "AdminPass123!", self.password_checker)
            print("5. Пользователь 'admin' зарегистрирован")

            auth_result = self.auth_system.authenticate("admin", "AdminPass123!")
            print(f"6. Аутентификация: {'Успешно' if auth_result else 'Неудачно'}")

            # Пробуем неправильный пароль
            wrong_auth = self.auth_system.authenticate("admin", "WrongPassword")
            print(f"7. Аутентификация с неправильным паролем: {'Успешно' if wrong_auth else 'Неудачно'}")

        except AuthenticationException as e:
            print(f"Ошибка аутентификации: {e}")

        # Демонстрация работы приложений
        text_editor_result = self.text_editor.start()
        print(f"8. {text_editor_result}")

        file_opened = self.text_editor.open_file("document.txt")
        print(f"9. {file_opened}")

        file_saved = self.text_editor.save_file("Содержимое файла")
        print(f"10. {file_saved}")

        # Демонстрация сетевых возможностей
        self.wifi.enable()
        wifi_networks = self.wifi.scan_networks()
        print(f"11. Найдено WiFi сетей: {len(wifi_networks)}")

        web_request = self.web_client.get_request("https://example.com")
        print(f"12. Веб-запрос: {web_request[:50]}...")

        # Демонстрация мониторинга
        self.monitor_system.add_metric("cpu_usage", 45.5)
        self.monitor_system.add_metric("memory_usage", 67.8)
        self.monitor_system.add_metric("temperature", 72.0)

        alerts = self.monitor_system.check_alerts()
        print(f"13. Активные алерты: {len(alerts)}")
        for alert in alerts:
            print(f"   - {alert}")

        # Демонстрация системы охлаждения
        self.cooling_system.adjust_cooling(75.0)
        print(f"14. Система охлаждения настроена на температуру 75°C")

        # Демонстрация информации о системе
        print(f"15. Процессор: {self.cpu.brand} {self.cpu.model}")
        print(f"16. Память: {self.ram.total_capacity} MB")
        print(f"17. Хранилище: {self.storage.capacity} MB")

        print("\n=== Демонстрация завершена ===")

    def get_key(self):
        """Метод для получения ключа шифрования (имитация)"""
        return b"secret_key_123456"


if __name__ == "__main__":
    # Создание и запуск компьютерной системы
    computer = ComputerSystem()
    computer.demonstrate_functionality()