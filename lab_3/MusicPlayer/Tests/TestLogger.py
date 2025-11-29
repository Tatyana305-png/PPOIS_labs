import unittest
import sys
import os
import tempfile
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Logger import Logger


class TestLogger(unittest.TestCase):

    def setUp(self):
        # Создаем временную директорию для логов
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test.log")

        # Создаем логгер с тестовым файлом
        self.logger = Logger()
        self.logger.log_file = self.log_file

    def tearDown(self):
        # Удаляем временную директорию
        shutil.rmtree(self.test_dir)

    def test_logger_initialization(self):
        """Тест инициализации логгера"""
        self.assertEqual(self.logger.log_file, self.log_file)

    def test_log_info(self):
        """Тест логирования INFO уровня"""
        test_message = "Test info message"
        self.logger.log(test_message, "INFO")

        # Проверяем запись в файл
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn("[INFO]", log_content)
        self.assertIn(test_message, log_content)
        # Проверяем формат временной метки
        self.assertRegex(log_content, r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]')

    def test_log_error(self):
        """Тест логирования ERROR уровня"""
        test_message = "Test error message"
        self.logger.log(test_message, "ERROR")

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn("[ERROR]", log_content)
        self.assertIn(test_message, log_content)

    def test_log_warning(self):
        """Тест логирования WARNING уровня"""
        test_message = "Test warning message"
        self.logger.log(test_message, "WARNING")

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn("[WARNING]", log_content)
        self.assertIn(test_message, log_content)

    def test_log_default_level(self):
        """Тест логирования с уровнем по умолчанию"""
        test_message = "Test default level message"
        self.logger.log(test_message)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn("[INFO]", log_content)
        self.assertIn(test_message, log_content)

    def test_multiple_logs(self):
        """Тест множественных записей в лог"""
        messages = ["First message", "Second message", "Third message"]

        for msg in messages:
            self.logger.log(msg)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()

        self.assertEqual(len(log_lines), 3)
        for i, line in enumerate(log_lines):
            self.assertIn(messages[i], line)

    def test_log_special_characters(self):
        """Тест логирования сообщений со специальными символами"""
        special_message = 'Test with "quotes" and regular text'
        self.logger.log(special_message)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn('"quotes"', log_content)

    def test_log_file_creation(self):
        """Тест создания файла лога"""
        # Файл должен создаваться при первой записи
        self.assertFalse(os.path.exists(self.log_file))

        self.logger.log("Test message")

        self.assertTrue(os.path.exists(self.log_file))


if __name__ == '__main__':
    unittest.main()