import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import ConstGraphIterator


class TestConstGraphIterator(unittest.TestCase):
    """Тесты для класса ConstGraphIterator"""

    def test_const_iterator_creation(self):
        """Тест создания константного итератора"""
        data = [1, 2, 3, 4, 5]
        iterator = ConstGraphIterator(data)

        self.assertEqual(iterator._data, data)
        self.assertEqual(iterator._index, 0)

    def test_const_iterator_iteration(self):
        """Тест итерации по элементам (только чтение)"""
        data = [1, 2, 3, 4, 5]
        iterator = ConstGraphIterator(data)

        # Используем цикл for
        result = []
        for item in iterator:
            result.append(item)

        self.assertEqual(result, data)

    def test_const_iterator_next(self):
        """Тест метода next"""
        data = ["a", "b", "c"]
        iterator = ConstGraphIterator(data)

        self.assertEqual(next(iterator), "a")
        self.assertEqual(next(iterator), "b")
        self.assertEqual(next(iterator), "c")

        # После конца данных должно быть StopIteration
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_const_iterator_current(self):
        """Тест метода current"""
        data = [10, 20, 30]
        iterator = ConstGraphIterator(data)

        # До первого next() current() должен вызывать ошибку
        with self.assertRaises(IndexError):
            iterator.current()

        # После первого next()
        next(iterator)
        self.assertEqual(iterator.current(), 10)

        # После второго next()
        next(iterator)
        self.assertEqual(iterator.current(), 20)

    def test_const_iterator_has_next(self):
        """Тест метода has_next"""
        data = [1, 2]
        iterator = ConstGraphIterator(data)

        self.assertTrue(iterator.has_next())  # Есть первый элемент
        next(iterator)

        self.assertTrue(iterator.has_next())  # Есть второй элемент
        next(iterator)

        self.assertFalse(iterator.has_next())  # Больше нет элементов

    def test_const_iterator_reset(self):
        """Тест метода reset"""
        data = [1, 2, 3]
        iterator = ConstGraphIterator(data)

        # Проходим часть элементов
        next(iterator)
        next(iterator)
        self.assertEqual(iterator._index, 2)

        # Сбрасываем
        iterator.reset()
        self.assertEqual(iterator._index, 0)
        self.assertEqual(next(iterator), 1)

    def test_const_iterator_read_only(self):
        """Тест, что итератор только для чтения не модифицирует данные"""
        data = [1, 2, 3]
        iterator = ConstGraphIterator(data)

        # Проходим по всем элементам
        list(iterator)

        # Данные не должны измениться
        self.assertEqual(data, [1, 2, 3])

        # Попытка модификации данных через итератор не должна быть доступна
        # (это проверяется тем, что нет методов для модификации)

    def test_const_iterator_empty_data(self):
        """Тест константного итератора с пустыми данными"""
        iterator = ConstGraphIterator([])

        self.assertFalse(iterator.has_next())
        with self.assertRaises(StopIteration):
            next(iterator)

        with self.assertRaises(IndexError):
            iterator.current()

    def test_const_iterator_size(self):
        """Тест метода size"""
        test_cases = [
            ([], 0),
            ([1], 1),
            (["a", "b", "c"], 3),
            (list(range(100)), 100),
        ]

        for data, expected_size in test_cases:
            iterator = ConstGraphIterator(data)
            self.assertEqual(iterator.size(), expected_size)

    def test_const_iterator_with_complex_objects(self):
        """Тест константного итератора со сложными объектами"""

        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        points = [Point(1, 2), Point(3, 4), Point(5, 6)]
        iterator = ConstGraphIterator(points)

        result = []
        for point in iterator:
            result.append((point.x, point.y))

        self.assertEqual(result, [(1, 2), (3, 4), (5, 6)])


if __name__ == '__main__':
    unittest.main()