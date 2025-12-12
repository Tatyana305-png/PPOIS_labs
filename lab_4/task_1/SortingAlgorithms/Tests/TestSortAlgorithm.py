import unittest
from SortAlgorithm import SortAlgorithm
from typing import List


class MockSortAlgorithm(SortAlgorithm):
    """Мок-класс для тестирования базового класса"""

    def _sort_implementation(self, arr: List, compare) -> None:
        """Простая реализация для тестирования"""
        # Пузырьковая сортировка для тестирования
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if compare(arr[j], arr[j + 1]) > 0:
                    self._swap(arr, j, j + 1)


class TestSortAlgorithm(unittest.TestCase):
    """Тесты для базового класса SortAlgorithm"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.algorithm = MockSortAlgorithm()

    def test_initialization(self):
        """Тест инициализации"""
        self.assertEqual(self.algorithm.comparisons_count, 0)
        self.assertEqual(self.algorithm.swaps_count, 0)

    def test_sort_empty_array(self):
        """Тест сортировки пустого массива"""
        arr = []
        self.algorithm.sort(arr)
        self.assertEqual(arr, [])
        self.assertEqual(self.algorithm.comparisons_count, 0)
        self.assertEqual(self.algorithm.swaps_count, 0)

    def test_sort_single_element(self):
        """Тест сортировки массива из одного элемента"""
        arr = [5]
        self.algorithm.sort(arr)
        self.assertEqual(arr, [5])
        self.assertEqual(self.algorithm.comparisons_count, 0)
        self.assertEqual(self.algorithm.swaps_count, 0)

    def test_sort_sorted_array(self):
        """Тест сортировки уже отсортированного массива"""
        arr = [1, 2, 3, 4, 5]
        self.algorithm.sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_sort_reverse_array(self):
        """Тест сортировки массива в обратном порядке"""
        arr = [5, 4, 3, 2, 1]
        self.algorithm.sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_sort_with_key(self):
        """Тест сортировки с ключевой функцией"""
        arr = ["aaa", "bb", "c"]
        self.algorithm.sort(arr, key=len)
        self.assertEqual(arr, ["c", "bb", "aaa"])

    def test_sort_reverse(self):
        """Тест обратной сортировки"""
        arr = [1, 3, 2, 5, 4]
        self.algorithm.sort(arr, reverse=True)
        self.assertEqual(arr, [5, 4, 3, 2, 1])

    def test_sort_with_key_and_reverse(self):
        """Тест сортировки с ключом и обратным порядком"""
        arr = ["aaa", "bb", "c"]
        self.algorithm.sort(arr, key=len, reverse=True)
        self.assertEqual(arr, ["aaa", "bb", "c"])

    def test_invalid_input_type(self):
        """Тест с неверным типом входных данных"""
        with self.assertRaises(TypeError):
            self.algorithm.sort("not a list")

    def test_swap_method(self):
        """Тест метода обмена"""
        arr = [1, 2, 3, 4]
        self.algorithm._swap(arr, 0, 1)
        self.assertEqual(arr, [2, 1, 3, 4])
        self.assertEqual(self.algorithm.swaps_count, 1)

        # Обмен одинаковых индексов
        self.algorithm._swap(arr, 2, 2)
        self.assertEqual(arr, [2, 1, 3, 4])
        self.assertEqual(self.algorithm.swaps_count, 1)  # Не должно увеличиться

    def test_default_compare(self):
        """Тест функции сравнения по умолчанию"""
        self.assertEqual(self.algorithm._default_compare(1, 2), -1)
        self.assertEqual(self.algorithm._default_compare(2, 1), 1)
        self.assertEqual(self.algorithm._default_compare(1, 1), 0)

        # Проверка счетчика сравнений
        self.assertEqual(self.algorithm.comparisons_count, 3)

    def test_get_stats(self):
        """Тест получения статистики"""
        arr = [3, 1, 2]
        self.algorithm.sort(arr)
        stats = self.algorithm.get_stats()

        self.assertEqual(stats['algorithm'], 'MockSortAlgorithm')
        self.assertGreater(stats['comparisons'], 0)
        self.assertGreater(stats['swaps'], 0)


if __name__ == "__main__":
    unittest.main()