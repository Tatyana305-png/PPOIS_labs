import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import GraphIterator


class TestGraphIterator(unittest.TestCase):
    """Тесты для класса GraphIterator"""

    def test_iterator_creation(self):
        """Тест создания итератора"""
        data = [1, 2, 3, 4, 5]
        iterator = GraphIterator(data)

        self.assertEqual(iterator._data, data)
        self.assertEqual(iterator._index, 0)

    def test_iterator_iteration(self):
        """Тест итерации по элементам"""
        data = [1, 2, 3, 4, 5]
        iterator = GraphIterator(data)

        # Используем цикл for
        result = []
        for item in iterator:
            result.append(item)

        self.assertEqual(result, data)

    def test_iterator_next(self):
        """Тест метода next"""
        data = ["a", "b", "c"]
        iterator = GraphIterator(data)

        self.assertEqual(next(iterator), "a")
        self.assertEqual(next(iterator), "b")
        self.assertEqual(next(iterator), "c")

        # После конца данных должно быть StopIteration
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_iterator_current(self):
        """Тест метода current"""
        data = [10, 20, 30]
        iterator = GraphIterator(data)

        # До первого next() current() должен вызывать ошибку
        with self.assertRaises(IndexError):
            iterator.current()

        # После первого next()
        next(iterator)
        self.assertEqual(iterator.current(), 10)

        # После второго next()
        next(iterator)
        self.assertEqual(iterator.current(), 20)

    def test_iterator_has_next(self):
        """Тест метода has_next"""
        data = [1, 2]
        iterator = GraphIterator(data)

        self.assertTrue(iterator.has_next())  # Есть первый элемент
        next(iterator)

        self.assertTrue(iterator.has_next())  # Есть второй элемент
        next(iterator)

        self.assertFalse(iterator.has_next())  # Больше нет элементов

    def test_iterator_reversed(self):
        """Тест создания обратного итератора"""
        data = [1, 2, 3]
        iterator = GraphIterator(data)

        reverse_iterator = reversed(iterator)

        # Проверяем, что это действительно обратный итератор
        from Iterators import ReverseGraphIterator
        self.assertIsInstance(reverse_iterator, ReverseGraphIterator)

        # Проверяем обратную итерацию
        result = list(reverse_iterator)
        self.assertEqual(result, [3, 2, 1])

    def test_iterator_empty_data(self):
        """Тест итератора с пустыми данными"""
        iterator = GraphIterator([])

        self.assertFalse(iterator.has_next())
        with self.assertRaises(StopIteration):
            next(iterator)

        with self.assertRaises(IndexError):
            iterator.current()

    def test_iterator_size(self):
        """Тест метода size"""
        test_cases = [
            ([], 0),
            ([1], 1),
            (["a", "b", "c"], 3),
            (list(range(100)), 100),
        ]

        for data, expected_size in test_cases:
            iterator = GraphIterator(data)
            self.assertEqual(iterator.size(), expected_size)


if __name__ == '__main__':
    unittest.main()