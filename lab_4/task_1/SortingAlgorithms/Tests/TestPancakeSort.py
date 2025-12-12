import unittest
from PancakeSort import PancakeSort
from StudentFactory import StudentFactory


class TestPancakeSort(unittest.TestCase):
    """Тесты для класса PancakeSort"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.sorter = PancakeSort()
        self.factory = StudentFactory()

    def test_initialization(self):
        """Тест инициализации"""
        self.assertIsInstance(self.sorter, PancakeSort)
        self.assertEqual(str(self.sorter), "Pancake Sort (сортировка переворотами)")

    def test_sort_numbers(self):
        """Тест сортировки чисел"""
        test_cases = [
            ([], []),
            ([1], [1]),
            ([2, 1], [1, 2]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([3, 1, 4, 1, 5, 9, 2, 6], [1, 1, 2, 3, 4, 5, 6, 9]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ]

        for input_arr, expected in test_cases:
            with self.subTest(input=input_arr):
                arr = input_arr.copy()
                self.sorter.sort(arr)
                self.assertEqual(arr, expected)

    def test_sort_strings(self):
        """Тест сортировки строк"""
        arr = ["банан", "яблоко", "апельсин", "киви"]
        expected = ["апельсин", "банан", "киви", "яблоко"]

        self.sorter.sort(arr)
        self.assertEqual(arr, expected)

    def test_sort_with_key(self):
        """Тест сортировки с ключевой функцией"""
        arr = ["aaa", "bb", "c"]
        self.sorter.sort(arr, key=len)
        self.assertEqual(arr, ["c", "bb", "aaa"])

    def test_sort_reverse(self):
        """Тест обратной сортировки"""
        arr = [1, 3, 2, 5, 4]
        self.sorter.sort(arr, reverse=True)
        self.assertEqual(arr, [5, 4, 3, 2, 1])

    def test_sort_students(self):
        """Тест сортировки студентов"""
        students = self.factory.create_sample_students()
        students_copy = students.copy()

        # Сортировка по имени
        self.sorter.sort(students_copy, key=lambda s: s.name)

        # Проверяем, что отсортировано правильно
        for i in range(len(students_copy) - 1):
            self.assertLessEqual(students_copy[i].name, students_copy[i + 1].name)

    def test_sort_students_by_gpa(self):
        """Тест сортировки студентов по GPA"""
        students = self.factory.create_sample_students()
        students_copy = students.copy()

        # Сортировка по GPA (по убыванию)
        self.sorter.sort(students_copy, key=lambda s: s.gpa, reverse=True)

        # Проверяем, что отсортировано правильно
        for i in range(len(students_copy) - 1):
            self.assertGreaterEqual(students_copy[i].gpa, students_copy[i + 1].gpa)

    def test_statistics(self):
        """Тест сбора статистики"""
        arr = [5, 3, 4, 1, 2]
        self.sorter.sort(arr)

        stats = self.sorter.get_stats()
        self.assertEqual(stats['algorithm'], 'PancakeSort')
        self.assertGreater(stats['comparisons'], 0)
        self.assertGreater(stats['swaps'], 0)

        # Проверяем, что массив отсортирован
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_find_max_index(self):
        """Тест поиска максимального элемента"""
        arr = [1, 5, 3, 2, 4]

        # Создаем простую функцию сравнения
        def compare(a, b):
            return -1 if a < b else 1 if a > b else 0

        max_index = self.sorter._find_max_index(arr, compare)
        self.assertEqual(max_index, 1)  # Элемент 5 на позиции 1

    def test_flip_method(self):
        """Тест метода переворота"""
        arr = [1, 2, 3, 4, 5]

        # Переворачиваем первые 3 элемента
        self.sorter._flip(arr, 2)
        self.assertEqual(arr, [3, 2, 1, 4, 5])
        self.assertEqual(self.sorter.swaps_count, 1)  # Было 3 обмена, но учитывается как 1

    def test_large_array(self):
        """Тест сортировки большого массива"""
        import random
        arr = [random.randint(0, 100) for _ in range(50)]
        arr_copy = arr.copy()

        self.sorter.sort(arr)
        arr_copy.sort()

        self.assertEqual(arr, arr_copy)

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Все элементы одинаковые
        arr = [5, 5, 5, 5]
        self.sorter.sort(arr)
        self.assertEqual(arr, [5, 5, 5, 5])

        # Отрицательные числа
        arr = [-5, -1, -3, -2, -4]
        self.sorter.sort(arr)
        self.assertEqual(arr, [-5, -4, -3, -2, -1])

        # Смешанные типы (не должны сравниваться)
        arr = [1, 2.5, 3]
        self.sorter.sort(arr)
        self.assertEqual(arr, [1, 2.5, 3])


if __name__ == "__main__":
    unittest.main()