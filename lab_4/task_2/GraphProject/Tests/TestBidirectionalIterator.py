import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Iterators import BidirectionalIterator


class TestBidirectionalIterator(unittest.TestCase):
    """Тесты для класса BidirectionalIterator"""

    def test_bidirectional_iterator_creation(self):
        """Тест создания двунаправленного итератора"""
        data = [1, 2, 3, 4, 5]
        iterator = BidirectionalIterator(data)

        self.assertEqual(iterator._data, data)
        self.assertEqual(iterator._index, 0)

    def test_bidirectional_iterator_previous(self):
        """Тест метода previous"""
        data = [1, 2, 3]
        iterator = BidirectionalIterator(data)

        # Двигаемся вперед
        next(iterator)  # 1
        next(iterator)  # 2

        # Двигаемся назад
        self.assertEqual(iterator.previous(), 1)
        self.assertEqual(iterator._index, 1)  # Теперь указываем на элемент 1

        # Еще назад
        with self.assertRaises(IndexError):  # Нет предыдущего элемента
            iterator.previous()

    def test_bidirectional_iterator_peek_next(self):
        """Тест метода peek_next"""
        data = [10, 20, 30]
        iterator = BidirectionalIterator(data)

        # Peek без перемещения
        self.assertEqual(iterator.peek_next(), 10)
        self.assertEqual(iterator._index, 0)  # Индекс не изменился

        # Перемещаемся и peek снова
        next(iterator)  # 10
        self.assertEqual(iterator.peek_next(), 20)

        # Доходим до конца
        next(iterator)  # 20
        next(iterator)  # 30

        with self.assertRaises(IndexError):  # Нет следующего элемента
            iterator.peek_next()

    def test_bidirectional_iterator_peek_previous(self):
        """Тест метода peek_previous"""
        data = [10, 20, 30]
        iterator = BidirectionalIterator(data)

        # В начале нет предыдущего
        with self.assertRaises(IndexError):
            iterator.peek_previous()

        # Двигаемся вперед и проверяем peek_previous
        next(iterator)  # 10
        with self.assertRaises(IndexError):  # После первого элемента нет предыдущего
            iterator.peek_previous()

        next(iterator)  # 20
        self.assertEqual(iterator.peek_previous(), 10)  # Можем заглянуть на предыдущий
        self.assertEqual(iterator._index, 2)  # Индекс не изменился

    def test_bidirectional_iterator_forward_backward(self):
        """Тест движения вперед и назад"""
        data = ["a", "b", "c", "d"]
        iterator = BidirectionalIterator(data)

        # Вперед
        self.assertEqual(next(iterator), "a")
        self.assertEqual(next(iterator), "b")

        # Назад
        self.assertEqual(iterator.previous(), "a")

        # Снова вперед
        self.assertEqual(next(iterator), "b")
        self.assertEqual(next(iterator), "c")

        # Назад два раза
        self.assertEqual(iterator.previous(), "b")
        self.assertEqual(iterator.previous(), "a")


    def test_bidirectional_iterator_edge_cases(self):
        """Тест граничных случаев"""
        # Пустой список
        iterator = BidirectionalIterator([])
        with self.assertRaises(StopIteration):
            next(iterator)

        # Один элемент
        iterator = BidirectionalIterator([42])
        self.assertEqual(next(iterator), 42)
        with self.assertRaises(IndexError):
            iterator.previous()
        with self.assertRaises(IndexError):
            iterator.peek_next()
        with self.assertRaises(IndexError):
            iterator.peek_previous()

    def test_bidirectional_iterator_inheritance(self):
        """Тест наследования от GraphIterator"""
        data = [1, 2, 3]
        iterator = BidirectionalIterator(data)

        # Проверяем, что наследует основные методы
        self.assertEqual(next(iterator), 1)
        self.assertEqual(iterator.current(), 1)
        self.assertTrue(iterator.has_next())

        # Проверяем reset
        iterator.reset()
        self.assertEqual(iterator._index, 0)

        # Проверяем size
        self.assertEqual(iterator.size(), 3)

        # Проверяем has_previous
        next(iterator)
        self.assertFalse(iterator.has_previous())
        next(iterator)
        self.assertTrue(iterator.has_previous())


if __name__ == '__main__':
    unittest.main()