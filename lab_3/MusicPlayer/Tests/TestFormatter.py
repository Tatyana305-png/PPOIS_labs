import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Formatter import Formatter


class TestFormatter(unittest.TestCase):

    def test_format_duration(self):
        """Тест форматирования длительности"""
        test_cases = [
            (0, "00:00"),
            (59, "00:59"),
            (60, "01:00"),
            (119, "01:59"),
            (120, "02:00"),
            (3599, "59:59"),
            (3600, "60:00"),
            (3661, "61:01"),
            (125.7, "02:05"),
        ]

        for seconds, expected in test_cases:
            with self.subTest(seconds=seconds, expected=expected):
                self.assertEqual(Formatter.format_duration(seconds), expected)

    def test_format_duration_edge_cases(self):
        """Тест граничных случаев форматирования длительности"""
        # Отрицательное время - тестируем реальное поведение
        self.assertEqual(Formatter.format_duration(-30), "-00:30")

        # Очень большое время
        self.assertEqual(Formatter.format_duration(999999), "16666:39")

    def test_format_file_size(self):
        """Тест форматирования размера файла"""
        test_cases = [
            (0, "0.0 B"),
            (500, "500.0 B"),
            (1023, "1023.0 B"),
            (1024, "1.0 KB"),
            (1536, "1.5 KB"),
            (1048576, "1.0 MB"),
            (1572864, "1.5 MB"),
            (1073741824, "1.0 GB"),
            (1610612736, "1.5 GB"),
        ]

        for bytes_size, expected in test_cases:
            with self.subTest(bytes=bytes_size, expected=expected):
                self.assertEqual(Formatter.format_file_size(bytes_size), expected)

    def test_format_file_size_edge_cases(self):
        """Тест граничных случаев форматирования размера файла"""
        # Отрицательный размер - тестируем реальное поведение
        # Текущая реализация форматирует -1024 как "-1.0 KB"
        self.assertEqual(Formatter.format_file_size(-1024), "-1.0 KB")


if __name__ == '__main__':
    unittest.main()