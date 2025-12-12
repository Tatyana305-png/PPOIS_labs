import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import BaseIterator


class TestBaseIterator(unittest.TestCase):
    """Тесты для базового класса BaseIterator"""

    def test_base_iterator_creation(self):
        """Тест создания базового итератора"""
        data = [1, 2, 3, 4, 5]
        iterator = BaseIterator(data)

        self.assertEqual(iterator._data, data)
        self.assertEqual(iterator._index, 0)

    def test_base_iterator_size(self):
        """Тест метода size"""
        test_cases = [
            ([], 0),
            ([1], 1),
            ([1, 2, 3], 3),
            (list(range(10)), 10),
        ]

        for data, expected_size in test_cases:
            iterator = BaseIterator(data)
            self.assertEqual(iterator.size(), expected_size)

    def test_base_iterator_get_data(self):
        """Тест метода get_data"""
        data = [1, 2, 3, 4, 5]
        iterator = BaseIterator(data)

        # get_data должен возвращать копию данных
        copied_data = iterator.get_data()
        self.assertEqual(copied_data, data)
        self.assertIsNot(copied_data, data)  # Это должна быть копия

    def test_base_iterator_not_implemented(self):
        """Тест, что абстрактные методы не реализованы"""
        iterator = BaseIterator([1, 2, 3])

        # Проверяем, что абстрактные методы выбрасывают NotImplementedError
        with self.assertRaises(NotImplementedError):
            next(iterator)

        with self.assertRaises(NotImplementedError):
            iterator.current()

        with self.assertRaises(NotImplementedError):
            iterator.has_next()

        with self.assertRaises(NotImplementedError):
            iterator.reset()

    def test_base_iterator_repr(self):
        """Тест строкового представления"""
        data = [1, 2, 3]
        iterator = BaseIterator(data)

        # Проверяем, что repr содержит имя класса и состояние
        repr_str = repr(iterator)
        self.assertIn("BaseIterator", repr_str)
        self.assertIn("index=0", repr_str)
        self.assertIn("size=3", repr_str)

    def test_base_iterator_empty_data(self):
        """Тест с пустыми данными"""
        iterator = BaseIterator([])
        self.assertEqual(iterator.size(), 0)
        self.assertEqual(iterator.get_data(), [])


if __name__ == '__main__':
    unittest.main()