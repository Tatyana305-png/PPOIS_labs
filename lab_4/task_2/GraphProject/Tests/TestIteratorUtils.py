import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import IteratorUtils, GraphIterator, ConstGraphIterator, ReverseGraphIterator, BidirectionalIterator


class TestIteratorUtils(unittest.TestCase):
    """Тесты для класса IteratorUtils"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.utils = IteratorUtils()

    def test_to_list(self):
        """Тест метода to_list"""
        data = [1, 2, 3, 4, 5]
        iterator = GraphIterator(data)

        result = self.utils.to_list(iterator)
        self.assertEqual(result, data)
        self.assertIsInstance(result, list)

    def test_count(self):
        """Тест метода count"""
        test_cases = [
            ([], 0),
            ([1], 1),
            ([1, 2, 3], 3),
            (list(range(100)), 100),
        ]

        for data, expected_count in test_cases:
            iterator = GraphIterator(data)
            count = self.utils.count(iterator)
            self.assertEqual(count, expected_count)

    def test_find(self):
        """Тест метода find"""
        data = [1, 2, 3, 4, 5]
        iterator = GraphIterator(data)

        # Поиск существующего элемента
        self.assertTrue(self.utils.find(iterator, 3))

        # Поиск несуществующего элемента
        iterator.reset()
        self.assertFalse(self.utils.find(iterator, 10))

        # Поиск в пустом списке
        empty_iterator = GraphIterator([])
        self.assertFalse(self.utils.find(empty_iterator, 1))

    def test_apply(self):
        """Тест метода apply"""
        data = [1, 2, 3]
        iterator = GraphIterator(data)

        # Собираем результаты применения функции
        results = []

        def collect(x):
            results.append(x * 2)

        self.utils.apply(iterator, collect)
        self.assertEqual(results, [2, 4, 6])

    def test_make_iterator(self):
        """Тест метода make_iterator"""
        data = [1, 2, 3]
        iterator = self.utils.make_iterator(data)

        self.assertIsInstance(iterator, GraphIterator)
        self.assertEqual(list(iterator), data)

    def test_make_const_iterator(self):
        """Тест метода make_const_iterator"""
        data = [1, 2, 3]
        iterator = self.utils.make_const_iterator(data)

        self.assertIsInstance(iterator, ConstGraphIterator)
        self.assertEqual(list(iterator), data)

    def test_make_reverse_iterator(self):
        """Тест метода make_reverse_iterator"""
        data = [1, 2, 3]
        iterator = self.utils.make_reverse_iterator(data)

        self.assertIsInstance(iterator, ReverseGraphIterator)
        self.assertEqual(list(iterator), [3, 2, 1])

    def test_make_bidirectional_iterator(self):
        """Тест метода make_bidirectional_iterator"""
        data = [1, 2, 3]
        iterator = self.utils.make_bidirectional_iterator(data)

        self.assertIsInstance(iterator, BidirectionalIterator)
        self.assertEqual(list(iterator), data)

    def test_filter(self):
        """Тест метода filter"""
        data = list(range(10))  # [0, 1, 2, ..., 9]
        iterator = GraphIterator(data)

        # Фильтруем четные числа
        def is_even(x):
            return x % 2 == 0

        filtered = self.utils.filter(iterator, is_even)
        self.assertEqual(filtered, [0, 2, 4, 6, 8])

    def test_map(self):
        """Тест метода map"""
        data = [1, 2, 3, 4, 5]
        iterator = GraphIterator(data)

        # Умножаем каждый элемент на 2
        def double(x):
            return x * 2

        mapped = self.utils.map(iterator, double)
        self.assertEqual(mapped, [2, 4, 6, 8, 10])

    def test_utils_with_different_iterator_types(self):
        """Тест утилит с разными типами итераторов"""
        data = [1, 2, 3, 4, 5]

        # Тестируем с GraphIterator
        graph_iter = GraphIterator(data)
        self.assertEqual(self.utils.count(graph_iter), 5)

        # Тестируем с ReverseGraphIterator
        reverse_iter = ReverseGraphIterator(data)
        self.assertEqual(self.utils.count(reverse_iter), 5)

        # Тестируем с ConstGraphIterator
        const_iter = ConstGraphIterator(data)
        self.assertEqual(self.utils.count(const_iter), 5)

        # Тестируем с BidirectionalIterator
        bidir_iter = BidirectionalIterator(data)
        self.assertEqual(self.utils.count(bidir_iter), 5)

    def test_empty_data_handling(self):
        """Тест обработки пустых данных"""
        empty_iter = GraphIterator([])

        self.assertEqual(self.utils.to_list(empty_iter), [])
        self.assertEqual(self.utils.count(empty_iter), 0)
        self.assertFalse(self.utils.find(empty_iter, 1))

        # apply с пустыми данными не должен вызывать ошибку
        call_count = [0]

        def counter(x):
            call_count[0] += 1

        self.utils.apply(empty_iter, counter)
        self.assertEqual(call_count[0], 0)

        # filter и map с пустыми данными
        filtered = self.utils.filter(empty_iter, lambda x: True)
        self.assertEqual(filtered, [])

        mapped = self.utils.map(empty_iter, lambda x: x)
        self.assertEqual(mapped, [])


if __name__ == '__main__':
    unittest.main()