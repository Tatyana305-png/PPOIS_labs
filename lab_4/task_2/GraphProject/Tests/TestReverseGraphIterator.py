import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import ReverseGraphIterator


class TestReverseGraphIterator(unittest.TestCase):
    """Тесты для класса ReverseGraphIterator"""

    def test_reverse_iterator_creation(self):
        """Тест создания обратного итератора"""
        data = [1, 2, 3, 4, 5]
        iterator = ReverseGraphIterator(data)

        self.assertEqual(iterator._data, data)
        self.assertEqual(iterator._index, 4)  # Начинается с последнего элемента

    def test_reverse_iterator_iteration(self):
        """Тест обратной итерации"""
        data = [1, 2, 3, 4, 5]
        iterator = ReverseGraphIterator(data)

        result = []
        for item in iterator:
            result.append(item)

        self.assertEqual(result, [5, 4, 3, 2, 1])

    def test_reverse_iterator_next(self):
        """Тест метода next для обратного итератора"""
        data = ["a", "b", "c"]
        iterator = ReverseGraphIterator(data)

        self.assertEqual(next(iterator), "c")
        self.assertEqual(next(iterator), "b")
        self.assertEqual(next(iterator), "a")

        # После конца данных должно быть StopIteration
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_reverse_iterator_current(self):
        """Тест метода current для обратного итератора"""
        data = [10, 20, 30]
        iterator = ReverseGraphIterator(data)

        # До первого next() current() должен вызывать ошибку
        with self.assertRaises(IndexError):
            iterator.current()

        # После первого next()
        next(iterator)
        self.assertEqual(iterator.current(), 30)

        # После второго next()
        next(iterator)
        self.assertEqual(iterator.current(), 20)

    def test_reverse_iterator_has_next(self):
        """Тест метода has_next для обратного итератора"""
        data = [1, 2, 3]
        iterator = ReverseGraphIterator(data)

        self.assertTrue(iterator.has_next())  # Есть первый элемент (последний в массиве)
        next(iterator)  # 3

        self.assertTrue(iterator.has_next())  # Есть второй элемент
        next(iterator)  # 2

        self.assertTrue(iterator.has_next())  # Есть третий элемент
        next(iterator)  # 1

        self.assertFalse(iterator.has_next())  # Больше нет элементов

    def test_reverse_iterator_has_previous(self):
        """Тест метода has_previous для обратного итератора"""
        data = [1, 2, 3, 4]
        iterator = ReverseGraphIterator(data)

        # Начинаем с конца: индекс = 3 (элемент 4)
        self.assertFalse(iterator.has_previous())  # Нет предыдущего (это первый в обратном порядке)
        next(iterator)  # Берем 4, индекс становится 2

        self.assertFalse(iterator.has_previous())  # После 4 нет предыдущего
        next(iterator)  # Берем 3, индекс становится 1

        self.assertTrue(iterator.has_previous())  # После 3 есть предыдущий (4)

    def test_reverse_iterator_reset(self):
        """Тест метода reset для обратного итератора"""
        data = [1, 2, 3]
        iterator = ReverseGraphIterator(data)

        # Проходим часть элементов
        next(iterator)  # 3
        next(iterator)  # 2
        self.assertEqual(iterator._index, 0)  # Следующий будет 1

        # Сбрасываем
        iterator.reset()
        self.assertEqual(iterator._index, 2)  # Возвращаемся к началу (последний элемент)
        self.assertEqual(next(iterator), 3)

    def test_reverse_iterator_empty_data(self):
        """Тест обратного итератора с пустыми данными"""
        iterator = ReverseGraphIterator([])

        self.assertFalse(iterator.has_next())
        with self.assertRaises(StopIteration):
            next(iterator)

        with self.assertRaises(IndexError):
            iterator.current()

    def test_reverse_iterator_single_element(self):
        """Тест обратного итератора с одним элементом"""
        iterator = ReverseGraphIterator([42])

        self.assertTrue(iterator.has_next())
        self.assertEqual(next(iterator), 42)
        self.assertFalse(iterator.has_next())

        with self.assertRaises(StopIteration):
            next(iterator)

    def test_reverse_iterator_size(self):
        """Тест метода size для обратного итератора"""
        test_cases = [
            ([], 0),
            ([1], 1),
            (["a", "b", "c"], 3),
            (list(range(100)), 100),
        ]

        for data, expected_size in test_cases:
            iterator = ReverseGraphIterator(data)
            self.assertEqual(iterator.size(), expected_size)


if __name__ == '__main__':
    unittest.main()