from Hardware.CPU.CPU import CPU
from Hardware.CPU.CPUCore import CPUCore
from Hardware.Memory.RAM import RAM
from Hardware.Memory.MemoryModule import MemoryModule
from Hardware.Storage.SSD import SSD
from Hardware.Storage.HardDrive import HardDrive
from Hardware.Storage.StorageDevice import StorageDevice
from Hardware.Motherboard.Motherboard import Motherboard
from Hardware.Motherboard.BIOS import BIOS
from Hardware.Peripherals.Keyboard import Keyboard
from Hardware.Peripherals.Mouse import Mouse
from Hardware.Peripherals.Monitor import Monitor
from Hardware.Peripherals.Peripheral import Peripheral

from Software.OS.OperatingSystem import OperatingSystem
from Software.OS.Kernel import Kernel
from Software.Applications.TextEditor import TextEditor
from Software.Applications.WebBrowser import WebBrowser
from Software.Applications.WebTab import WebTab
from Software.Applications.Application import Application
from Software.Security.SecurityManager import SecurityManager
from Software.Security.AuthenticationSystem import AuthenticationSystem
from Software.Security.PasswordChecker import PasswordChecker
from Software.Security.EncryptionProvider import EncryptionProvider
from Software.Utilities.FileManager import FileManager
from Software.Utilities.CompressionUtility import CompressionUtility
from Software.Utilities.SystemCleaner import SystemCleaner

from Network.Internet.InternetConnection import InternetConnection
from Network.Internet.WebClient import WebClient
from Network.Internet.EmailClient import EmailClient
from Network.WiFi.WiFiAdapter import WiFiAdapter
from Network.WiFi.BluetoothAdapter import BluetoothAdapter
from Network.Protocols.Protocol import Protocol
from Network.Protocols.HTTPProtocol import HTTPProtocol
from Network.Protocols.TCPProtocol import TCPProtocol

from System.Power.PowerSupply import PowerSupply
from System.Power.Battery import Battery
from System.Cooling.CoolingSystem import CoolingSystem
from System.Cooling.Fan import Fan
from System.Cooling.TemperatureSensor import TemperatureSensor
from System.Monitoring.SystemMonitor import SystemMonitor
from System.Monitoring.PerformanceCounter import PerformanceCounter

from Exceptions.CPUOverheatException import CPUOverheatException
from Exceptions.MemoryAllocationException import MemoryAllocationException
from Exceptions.StorageFullException import StorageFullException
from Exceptions.AuthenticationException import AuthenticationException
from Exceptions.EncryptionException import EncryptionException
from Exceptions.ApplicationCrashException import ApplicationCrashException


class ComputerSystem:
    def __init__(self):
        print("Инициализация компьютерной системы...")

        # Аппаратное обеспечение
        self._init_hardware()

        # Программное обеспечение
        self._init_software()

        # Сетевое взаимодействие
        self._init_network()

        # Системные компоненты
        self._init_system()

        # Настройка ассоциаций
        self._setup_associations()

        print("Компьютерная система готова к работе!")

    def _init_hardware(self):
        """Инициализация аппаратного обеспечения"""
        # Процессор и память
        self.cpu = CPU("Intel", "Core i9-13900K", 24, 5.8)
        self.ram = RAM(32768)  # 32GB
        memory_module1 = MemoryModule(16384, 5600, "DDR5")
        memory_module2 = MemoryModule(16384, 5600, "DDR5")
        self.ram.add_module(memory_module1)
        self.ram.add_module(memory_module2)

        # Хранилище
        self.ssd = SSD(2000000, "NVMe")  # 2TB SSD
        self.hdd = HardDrive(4000000, 7200)  # 4TB HDD

        # Материнская плата и BIOS
        self.motherboard = Motherboard("ASUS ROG Maximus", "Z790")
        self.bios = BIOS("2.1.5")

        # Периферия
        self.keyboard = Keyboard("QWERTY-RU", True)
        self.mouse = Mouse(3200, 6)
        self.monitor = Monitor((3840, 2160), 144)

    def _init_software(self):
        """Инициализация программного обеспечения"""
        # Операционная система
        self.os = OperatingSystem("Windows", "11 Pro")
        self.kernel = Kernel()

        # Безопасность
        self.security_manager = SecurityManager()
        self.auth_system = AuthenticationSystem()
        self.password_checker = PasswordChecker()
        self.encryption_provider = EncryptionProvider("AES-256")

        # Приложения
        self.text_editor = TextEditor()
        self.web_browser = WebBrowser()

        # Утилиты
        self.file_manager = FileManager()
        self.compression_utility = CompressionUtility()
        self.system_cleaner = SystemCleaner()

    def _init_network(self):
        """Инициализация сетевого взаимодействия"""
        self.internet_connection = InternetConnection("Fiber", 1000)
        self.web_client = WebClient()
        self.email_client = EmailClient()
        self.wifi_adapter = WiFiAdapter("Wi-Fi 6E", "6GHz")
        self.bluetooth_adapter = BluetoothAdapter("5.3")

        # Сетевые протоколы
        self.http_protocol = HTTPProtocol()
        self.tcp_protocol = TCPProtocol()

    def _init_system(self):
        """Инициализация системных компонентов"""
        # Питание
        self.power_supply = PowerSupply(1200, "80+ Platinum")
        self.battery = Battery(99000, "Li-Polymer")

        # Охлаждение
        self.cooling_system = CoolingSystem()
        self.cpu_fan = Fan(120, 2200)
        self.case_fan1 = Fan(140, 1500)
        self.case_fan2 = Fan(140, 1500)
        self.cpu_temp_sensor = TemperatureSensor("CPU")
        self.gpu_temp_sensor = TemperatureSensor("GPU")

        # Мониторинг
        self.system_monitor = SystemMonitor()
        self.cpu_performance_counter = PerformanceCounter("cpu_usage")
        self.memory_performance_counter = PerformanceCounter("memory_usage")

    def _setup_associations(self):
        """Настройка ассоциаций между компонентами"""
        # Аппаратные ассоциации
        self.motherboard.install_cpu(self.cpu)
        self.motherboard.install_ram(self.ram, 0)

        # Добавление компонентов охлаждения
        self.cooling_system.add_fan(self.cpu_fan)
        self.cooling_system.add_fan(self.case_fan1)
        self.cooling_system.add_fan(self.case_fan2)
        self.cooling_system.temperature_sensors.append(self.cpu_temp_sensor)
        self.cooling_system.temperature_sensors.append(self.gpu_temp_sensor)

        # Программные ассоциации
        self.os.security_module = self.security_manager
        self.security_manager.encryption_providers.append(self.encryption_provider)
        self.security_manager.authentication_methods['password'] = self.auth_system
        self.auth_system.password_validator = self.password_checker

        # Установка приложений в ОС
        self.os.install_application(self.text_editor)
        self.os.install_application(self.web_browser)

        # Настройка веб-браузера
        self.web_browser.download_manager = self.file_manager

        # Настройка мониторинга
        self.system_monitor.performance_counters['cpu'] = self.cpu_performance_counter
        self.system_monitor.performance_counters['memory'] = self.memory_performance_counter

    def demonstrate_functionality(self):
        """Демонстрация функциональности всей системы"""
        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ ФУНКЦИОНАЛЬНОСТИ КОМПЬЮТЕРНОЙ СИСТЕМЫ")
        print("=" * 60)

        self._demo_hardware()
        self._demo_software()
        self._demo_network()
        self._demo_system()
        self._demo_integration()

        print("\nДемонстрация завершена!")

    def _demo_hardware(self):
        """Демонстрация аппаратного обеспечения"""
        print("\n🔧 АППАРАТНОЕ ОБЕСПЕЧЕНИЕ:")
        print("-" * 40)

        # Демонстрация процессора
        try:
            instruction_result = self.cpu.execute_instruction("ADD R1, R2")
            print(f"1. CPU: {instruction_result}")
            print(f"   Температура CPU: {self.cpu.get_temperature()}°C")
        except CPUOverheatException as e:
            print(f"    {e}")

        # Демонстрация памяти
        if self.ram.modules:
            memory_address = self.ram.modules[0].allocate_memory(2048, "demo_process")
            print(f"2. Память: Выделено 2KB по адресу {memory_address}")
            print(f"   Всего модулей памяти: {len(self.ram.modules)}")

        # Демонстрация хранилища
        try:
            self.ssd.store_file("demo.txt", b"Hello, Computer System!")
            file_content = self.ssd.read_file("demo.txt")
            print(f"3. SSD: Файл записан и прочитан: {file_content.decode()}")
        except StorageFullException as e:
            print(f"    {e}")

        # Демонстрация периферии
        self.keyboard.key_press("A")
        self.keyboard.key_press("B")
        self.keyboard.key_press("Enter")
        print(f"4. Клавиатура: Нажаты клавиши: {self.keyboard.get_key_combination()}")

        mouse_position = self.mouse.move(100, 200)
        print(f"5. Мышь: Перемещена в позицию {mouse_position}")

    def _demo_software(self):
        """Демонстрация программного обеспечения"""
        print("\nПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ:")
        print("-" * 40)

        # Демонстрация ОС
        self.os.boot()
        process_id = self.os.run_application("TextEditor")
        print(f"1. ОС: Запущен процесс {process_id}")

        # Демонстрация безопасности
        try:
            self.auth_system.register_user("admin", "AdminPass123!", self.password_checker)
            auth_result = self.auth_system.authenticate("admin", "AdminPass123!")
            print(f"2. Безопасность: Аутентификация {'успешна' if auth_result else 'неудачна'}")
        except AuthenticationException as e:
            print(f"    {e}")

        # Демонстрация приложений
        self.text_editor.open_file("document.txt")
        save_result = self.text_editor.save_file("Содержимое документа")
        print(f"3. Текстовый редактор: {save_result}")

        # Демонстрация шифрования
        try:
            test_data = b"Secret data for encryption"
            encrypted = self.encryption_provider.encrypt(test_data, self)
            decrypted = self.encryption_provider.decrypt(encrypted, self)
            print(f"4. Шифрование: Данные успешно зашифрованы и расшифрованы")
            print(f"   Исходные: {test_data[:20]}... → Зашифрованные: {encrypted[:20]}...")
        except EncryptionException as e:
            print(f"    {e}")

    def _demo_network(self):
        """Демонстрация сетевого взаимодействия"""
        print("\n СЕТЕВОЕ ВЗАИМОДЕЙСТВИЕ:")
        print("-" * 40)

        # Демонстрация интернет-соединения
        self.internet_connection.connect()
        status = self.internet_connection.get_connection_status()
        print(f"1. Интернет: {status['type']} соединение, скорость {status['speed']} Mbps")

        # Демонстрация WiFi
        self.wifi_adapter.enable()
        networks = self.wifi_adapter.scan_networks()
        print(f"2. WiFi: Найдено {len(networks)} сетей")

        # Демонстрация веб-клиента
        web_request = self.web_client.get_request("https://example.com/api/data")
        print(f"3. Веб-клиент: GET запрос создан ({len(web_request)} символов)")

        # Демонстрация Bluetooth
        self.bluetooth_adapter.enable()
        self.bluetooth_adapter.pair_device("Wireless Headphones", "AA:BB:CC:11:22:33")
        print(f"4. Bluetooth: Устройство сопряжено")

    def _demo_system(self):
        """Демонстрация системных компонентов"""
        print("\n СИСТЕМНЫЕ КОМПОНЕНТЫ:")
        print("-" * 40)

        try:
            # Демонстрация питания - используем атрибуты напрямую
            self.power_supply.turn_on()
            print(f"1. Блок питания: {self.power_supply.wattage}W, {self.power_supply.efficiency_rating}")
        except Exception as e:
            print(f"1. Блок питания: информация недоступна ({e})")

        try:
            # Демонстрация батареи - используем атрибуты напрямую
            print(f"2. Батарея: {self.battery.capacity}mAh, тип {self.battery.battery_type}")
        except Exception as e:
            print(f"2. Батарея: информация недоступна ({e})")

        try:
            # Демонстрация охлаждения
            self.cpu_temp_sensor.update_temperature(65.0)
            self.gpu_temp_sensor.update_temperature(72.0)

            # Получаем температуры напрямую из сенсоров
            cpu_temp = self.cpu_temp_sensor.current_temperature
            gpu_temp = self.gpu_temp_sensor.current_temperature
            print(f"3. Охлаждение: CPU {cpu_temp}°C, GPU {gpu_temp}°C")

            # Показываем вентиляторы
            print(f"   Установлено вентиляторов: {len(self.cooling_system.fans)}")

        except Exception as e:
            print(f"3. Охлаждение: информация недоступна ({e})")

        try:
            # Демонстрация мониторинга
            self.system_monitor.add_metric("cpu_usage", 45.5)
            self.system_monitor.add_metric("memory_usage", 67.8)
            self.system_monitor.add_metric("temperature", 68.0)

            # Простая демонстрация мониторинга
            print(f"4. Мониторинг: отслеживается {len(self.system_monitor.performance_counters)} метрик")
            print(f"   Счетчики производительности: {list(self.system_monitor.performance_counters.keys())}")

        except Exception as e:
            print(f"4. Мониторинг: информация недоступна ({e})")

    def _demo_integration(self):
        """Демонстрация интеграции компонентов"""
        print("\nИНТЕГРАЦИЯ КОМПОНЕНТОВ:")
        print("-" * 40)

        # Комплексный сценарий: работа пользователя
        print("1. Пользователь запускает веб-браузер...")
        browser_tab = self.web_browser.open_tab("https://example.com")
        print(f"   Открыта вкладка: {browser_tab.url}")

        print("2. Пользователь работает с текстовым редактором...")
        self.text_editor.open_file("notes.txt")
        self.text_editor.save_file("Важные заметки о проекте")

        print("3. Система мониторинга отслеживает производительность...")
        self.cpu_performance_counter.add_sample(42.3)
        self.memory_performance_counter.add_sample(71.2)

        avg_cpu = self.cpu_performance_counter.get_average(5)
        avg_memory = self.memory_performance_counter.get_average(5)
        print(f"   Средняя загрузка CPU: {avg_cpu:.1f}%")
        print(f"   Средняя загрузка памяти: {avg_memory:.1f}%")

        print("4. Система охлаждения регулирует работу...")
        self.cooling_system.adjust_cooling(75.0)
        print(f"   Скорость вентиляторов установлена")

    def get_key(self):
        """Метод для получения ключа шифрования"""
        return b"secure_encryption_key_256bit"

    def system_info(self):
        """Вывод информации о системе"""
        print("\n" + "=" * 60)
        print("ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 60)

        print(f"Аппаратное обеспечение:")
        print(f"   • Процессор: {self.cpu.brand} {self.cpu.model}")
        print(f"   • Память: {self.ram.total_capacity} MB")
        print(f"   • SSD: {self.ssd.capacity} MB")
        print(f"   • HDD: {self.hdd.capacity} MB")

        print(f"Программное обеспечение:")
        print(f"   • ОС: {self.os.name} {self.os.version}")
        print(f"   • Приложения: {len(self.os.installed_applications)} установлено")

        print(f"Сетевое взаимодействие:")
        print(f"   • Интернет: {self.internet_connection.connection_type}")
        print(f"   • WiFi: {self.wifi_adapter.standard}")

        print(f"Системные компоненты:")
        print(f"   • Блок питания: {self.power_supply.wattage}W")
        print(f"   • Вентиляторы: {len(self.cooling_system.fans)} шт.")


class MockKeyManager:
    """Менеджер ключей для тестирования шифрования"""

    def get_key(self):
        return b"test_key_123456789012345678901234567890"


def main():
    """Главная функция для запуска системы"""
    # Создание и запуск компьютерной системы
    computer = ComputerSystem()

    # Вывод информации о системе
    computer.system_info()

    # Демонстрация функциональности
    computer.demonstrate_functionality()


if __name__ == "__main__":
    main()
