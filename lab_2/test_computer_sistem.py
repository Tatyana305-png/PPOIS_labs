import unittest
import sys
import os
from datetime import datetime
from computer_system import *


class TestComputerSystem(unittest.TestCase):
    """Тесты для компьютерной системы"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.computer = Computer()
        # Создаем тестового пользователя напрямую для тестов
        test_user = User("test_user", str(hash("test_password")))
        self.computer.operating_system.security_manager.users["test_user"] = test_user

    def test_computer_initialization(self):
        """Тест инициализации компьютера"""
        self.assertIsNotNone(self.computer.cpu)
        self.assertIsNotNone(self.computer.ram)
        self.assertIsNotNone(self.computer.hard_drive)
        self.assertIsNotNone(self.computer.operating_system)
        self.assertFalse(self.computer.is_running)

    def test_cpu_initialization(self):
        """Тест инициализации процессора"""
        cpu = self.computer.cpu
        self.assertEqual(cpu.name, "Core i9-13900K")
        self.assertEqual(cpu.cores, 24)
        self.assertEqual(cpu.speed, 5.8)
        self.assertEqual(cpu.usage, 0.0)
        self.assertIsInstance(cpu.cache_memory, CacheMemory)

    def test_ram_initialization(self):
        """Тест инициализации оперативной памяти"""
        ram = self.computer.ram
        self.assertEqual(ram.capacity, 64)
        self.assertEqual(ram.voltage, 1.5)
        self.assertIsInstance(ram.memory_controller, MemoryController)

    def test_power_on_success(self):
        """Тест успешного включения компьютера"""
        result = self.computer.power_on()
        self.assertTrue(result)
        self.assertTrue(self.computer.is_running)

    def test_login_success(self):
        """Тест успешной аутентификации"""
        self.computer.power_on()
        session = self.computer.login("test_user", "test_password")
        self.assertIsNotNone(session)
        self.assertTrue(session.is_active)
        self.assertEqual(session.user.username, "test_user")

    def test_login_failure(self):
        """Тест неудачной аутентификации"""
        self.computer.power_on()
        session = self.computer.login("wrong_user", "wrong_password")
        self.assertIsNone(session)

    def test_password_strength_check(self):
        """Тест проверки надежности пароля"""
        # Слабый пароль
        weak_result = self.computer.check_password_strength("123")
        self.assertFalse(weak_result["is_strong"])
        self.assertLess(weak_result["score"], 4)

        # Сильный пароль
        strong_result = self.computer.check_password_strength("StrongPass123!")
        self.assertTrue(strong_result["is_strong"])
        self.assertGreaterEqual(strong_result["score"], 4)

    def test_file_creation(self):
        """Тест создания файла"""
        file_system = self.computer.operating_system.file_system
        test_file = file_system.create_file("test.txt")

        self.assertEqual(test_file.filename, "test.txt")
        self.assertEqual(test_file.size, 0)
        self.assertIn("test.txt", file_system.files)

    def test_file_content_operations(self):
        """Тест операций с содержимым файла"""
        file_system = self.computer.operating_system.file_system
        test_file = file_system.create_file("test.txt")

        # Запись содержимого
        test_content = b"Hello, World!"
        test_file.write_content(test_content)

        self.assertEqual(test_file.size, len(test_content))
        self.assertEqual(test_file.read_content(), test_content)

    def test_duplicate_file_creation(self):
        """Тест создания дубликата файла"""
        file_system = self.computer.operating_system.file_system
        file_system.create_file("test.txt")

        with self.assertRaises(FileSystemError):
            file_system.create_file("test.txt")


class TestEncryption(unittest.TestCase):
    """Тесты системы шифрования"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.computer = Computer()
        test_user = User("test_user", str(hash("test_password")))
        self.computer.operating_system.security_manager.users["test_user"] = test_user
        self.computer.power_on()
        self.session = self.computer.login("test_user", "test_password")

    def test_aes_encryption_decryption(self):
        """Тест шифрования и дешифрования AES"""
        test_content = b"Test secret message for AES encryption"
        encrypted_file = self.computer.encrypt_file(
            "test_aes.txt", test_content, "AES", "test_key", self.session
        )

        self.assertEqual(encrypted_file.algorithm, "AES")
        self.assertGreater(encrypted_file.size, 0)

        # Дешифрование
        decrypted_file = self.computer.decrypt_file(encrypted_file, "test_key", self.session)
        self.assertEqual(decrypted_file.content, test_content)

    def test_xor_encryption_decryption(self):
        """Тест шифрования и дешифрования XOR"""
        test_content = b"Test secret message for XOR encryption"
        encrypted_file = self.computer.encrypt_file(
            "test_xor.txt", test_content, "XOR", "test_key", self.session
        )

        self.assertEqual(encrypted_file.algorithm, "XOR")

        # Дешифрование
        decrypted_file = self.computer.decrypt_file(encrypted_file, "test_key", self.session)
        self.assertEqual(decrypted_file.content, test_content)

    def test_caesar_encryption_decryption(self):
        """Тест шифрования и дешифрования Caesar"""
        test_content = b"Test secret message for Caesar encryption"
        encrypted_file = self.computer.encrypt_file(
            "test_caesar.txt", test_content, "CAESAR", "5", self.session
        )

        self.assertEqual(encrypted_file.algorithm, "CAESAR")

        # Дешифрование
        decrypted_file = self.computer.decrypt_file(encrypted_file, "5", self.session)
        self.assertEqual(decrypted_file.content, test_content)

    def test_wrong_decryption_key(self):
        """Тест дешифрования с неверным ключом"""
        test_content = b"Secret message"
        encrypted_file = self.computer.encrypt_file(
            "test_wrong_key.txt", test_content, "AES", "correct_key", self.session
        )

        with self.assertRaises(SecurityError):
            self.computer.decrypt_file(encrypted_file, "wrong_key", self.session)

    def test_encryption_with_invalid_algorithm(self):
        """Тест шифрования с неверным алгоритмом"""
        test_content = b"Test message"

        with self.assertRaises(SecurityError):
            self.computer.encrypt_file(
                "test_invalid.txt", test_content, "INVALID_ALGO", "key", self.session
            )

    def test_encryption_integrity(self):
        """Тест целостности данных при шифровании"""
        original_content = b"Original data that should remain unchanged after encryption and decryption"

        for algorithm in ["AES", "XOR", "CAESAR"]:
            with self.subTest(algorithm=algorithm):
                encrypted_file = self.computer.encrypt_file(
                    f"test_{algorithm}.txt", original_content, algorithm, "test_key", self.session
                )
                decrypted_file = self.computer.decrypt_file(encrypted_file, "test_key", self.session)
                self.assertEqual(decrypted_file.content, original_content)


class TestHardwareComponents(unittest.TestCase):
    """Тесты аппаратных компонентов"""

    def setUp(self):
        self.computer = Computer()

    def test_cpu_instruction_execution(self):
        """Тест выполнения инструкций процессором"""
        instruction = Instruction("ADD", ["R1", "R2"])
        result = self.computer.cpu.execute_instruction(instruction)
        self.assertTrue(result)
        self.assertGreater(self.computer.cpu.usage, 0)

    def test_cpu_overload(self):
        """Тест перегрузки процессора"""
        self.computer.cpu.usage = 99
        instruction = Instruction("MUL", ["R3", "R4"])

        with self.assertRaises(CPUError):
            self.computer.cpu.execute_instruction(instruction)

    def test_ram_read_write(self):
        """Тест чтения и записи в оперативную память"""
        test_data = b"Test data for RAM"
        address = 0x1000

        # Запись
        result = self.computer.ram.write_data(address, test_data)
        self.assertTrue(result)

        # Чтение
        read_data = self.computer.ram.read_data(address)
        self.assertEqual(read_data, test_data)

    def test_ram_invalid_address(self):
        """Тест чтения из неверного адреса памяти"""
        with self.assertRaises(MemoryAllocationError):
            self.computer.ram.read_data(0xFFFF)

    def test_component_diagnostics(self):
        """Тест диагностики компонентов"""
        self.assertTrue(self.computer.cpu.diagnose())
        self.assertTrue(self.computer.ram.diagnose())
        self.assertTrue(self.computer.gpu.diagnose())

    def test_power_supply(self):
        """Тест блока питания"""
        # Нормальная работа
        result = self.computer.power_supply.supply_power(self.computer.cpu)
        self.assertTrue(result)

        # Перегрузка (имитируем высокое напряжение)
        high_power_component = CPU("Test CPU", "Test", 1, 1.0)
        high_power_component.voltage = 100.0  # Очень высокое напряжение

        with self.assertRaises(HardwareError):
            self.computer.power_supply.supply_power(high_power_component)


class TestExceptions(unittest.TestCase):
    """Тесты исключений"""

    def setUp(self):
        self.computer = Computer()

    def test_memory_error(self):
        """Тест исключений памяти"""
        with self.assertRaises(MemoryAllocationError):
            self.computer.ram.read_data(999999)

    def test_cpu_error(self):
        """Тест исключений процессора"""
        self.computer.cpu.usage = 100

        with self.assertRaises(CPUError):
            self.computer.cpu.execute_instruction(Instruction("DIV", ["R1", "R2"]))


    def test_authentication_error(self):
        """Тест исключений аутентификации"""
        self.computer.power_on()

        with self.assertRaises(AuthenticationError):
            self.computer.operating_system.security_manager.authenticate_user(
                "nonexistent", "password"
            )

    def test_authorization_error(self):
        """Тест исключений авторизации"""
        test_user = User("test_user", str(hash("test_password")))
        session = UserSession(test_user)
        session.is_active = False  # Делаем сессию неактивной

        with self.assertRaises(AuthorizationError):
            self.computer.encrypt_file(
                "test.txt", b"data", "AES", "key", session
            )


class TestSystemIntegration(unittest.TestCase):
    """Интеграционные тесты системы"""

    def setUp(self):
        self.computer = Computer()
        test_user = User("test_user", str(hash("test_password")))
        self.computer.operating_system.security_manager.users["test_user"] = test_user

    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Включение компьютера
        self.assertTrue(self.computer.power_on())

        # Аутентификация
        session = self.computer.login("test_user", "test_password")
        self.assertIsNotNone(session)

        # Создание файла
        file_system = self.computer.operating_system.file_system
        test_file = file_system.create_file("workflow_test.txt")
        test_content = b"Integration test content"
        test_file.write_content(test_content)

        # Шифрование файла
        encrypted_file = self.computer.encrypt_file(
            "workflow_test.txt", test_content, "AES", "workflow_key", session
        )

        # Дешифрование файла
        decrypted_file = self.computer.decrypt_file(encrypted_file, "workflow_key", session)

        # Проверка целостности
        self.assertEqual(decrypted_file.content, test_content)

    def test_benchmark_performance(self):
        """Тест производительности шифрования"""
        self.computer.power_on()
        session = self.computer.login("test_user", "test_password")

        results = self.computer.benchmark_encryption(1024, session)  # 1KB данных

        self.assertIsInstance(results, dict)
        for algo, time in results.items():
            self.assertIn(algo, ["AES", "XOR", "CAESAR"])
            self.assertIsInstance(time, float)

    def test_system_info(self):
        """Тест получения информации о системе"""
        system_info = self.computer.get_system_info()

        expected_keys = ["CPU", "RAM", "GPU", "Hard Drive", "Motherboard", "Power Supply", "OS"]
        for key in expected_keys:
            self.assertIn(key, system_info)
            self.assertIsInstance(system_info[key], str)
            self.assertGreater(len(system_info[key]), 0)


class TestSecurityManager(unittest.TestCase):
    """Тесты менеджера безопасности"""

    def setUp(self):
        self.security_manager = SecurityManager()
        self.test_user = User("security_test_user", str(hash("security_test_pass")))
        self.security_manager.users["security_test_user"] = self.test_user

    def test_successful_authentication(self):
        """Тест успешной аутентификации"""
        session = self.security_manager.authenticate_user("security_test_user", "security_test_pass")
        self.assertIsNotNone(session)
        self.assertTrue(session.is_active)
        self.assertEqual(session.user.username, "security_test_user")

    def test_failed_authentication_wrong_password(self):
        """Тест неудачной аутентификации (неверный пароль)"""
        with self.assertRaises(AuthenticationError):
            self.security_manager.authenticate_user("security_test_user", "wrong_password")

    def test_failed_authentication_unknown_user(self):
        """Тест неудачной аутентификации (неизвестный пользователь)"""
        with self.assertRaises(AuthenticationError):
            self.security_manager.authenticate_user("unknown_user", "password")


class TestFileSystem(unittest.TestCase):
    """Тесты файловой системы"""

    def setUp(self):
        self.file_system = FileSystem("TEST_FS")

    def test_create_and_retrieve_file(self):
        """Тест создания и получения файла"""
        filename = "test_file.txt"
        file = self.file_system.create_file(filename)

        self.assertEqual(file.filename, filename)
        self.assertIn(filename, self.file_system.files)
        self.assertEqual(self.file_system.files[filename], file)

    def test_file_content_management(self):
        """Тест управления содержимым файла"""
        file = self.file_system.create_file("content_test.txt")

        # Изначально файл пустой
        self.assertEqual(file.size, 0)
        self.assertEqual(file.content, b"")

        # Запись содержимого
        test_content = b"This is test content"
        file.write_content(test_content)

        self.assertEqual(file.size, len(test_content))
        self.assertEqual(file.content, test_content)

        # Перезапись содержимого
        new_content = b"New test content"
        file.write_content(new_content)

        self.assertEqual(file.size, len(new_content))
        self.assertEqual(file.content, new_content)


def run_tests():
    """Запуск всех тестов с детализированным выводом"""
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тестовые классы
    test_classes = [
        TestComputerSystem,
        TestEncryption,
        TestHardwareComponents,
        TestExceptions,
        TestSystemIntegration,
        TestSecurityManager,
        TestFileSystem
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Запускаем тесты с детализированным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим итоговую статистику
    print("\n" + "=" * 60)
    print(" ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f" Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Провалено тестов: {len(result.failures)}")
    print(f" Ошибок: {len(result.errors)}")

    if result.failures:
        print("\n ПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.splitlines()[-1]}")

    if result.errors:
        print("\n ТЕСТЫ С ОШИБКАМИ:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.splitlines()[-1]}")

    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    print(" ЗАПУСК UNIT ТЕСТОВ ДЛЯ КОМПЬЮТЕРНОЙ СИСТЕМЫ")
    print("=" * 60)

    success = run_tests()

    if success:
        print("\n ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        sys.exit(0)
    else:
        print("\n НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ!")
        sys.exit(1)
