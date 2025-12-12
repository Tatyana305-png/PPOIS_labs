import unittest
from Smoothsort import Smoothsort
from StudentFactory import StudentFactory


class TestSmoothsort(unittest.TestCase):
    """Тесты для класса Smoothsort"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.sorter = Smoothsort()
        self.factory = StudentFactory()

    def test_initialization(self):
        """Тест инициализации"""
        self.assertIsInstance(self.sorter, Smoothsort)
        self.assertEqual(str(self.sorter), "Smoothsort (гладкая сортировка)")

    def test_build_leonardo_numbers(self):
        """Тест построения чисел Леонардо"""
        # Числа Леонардо: 1, 1, 3, 5, 9, 15, 25, 41, 67, 109, ...
        self.sorter._build_leonardo_numbers(20)
        numbers = self.sorter._leonardo_numbers
        self.assertGreaterEqual(len(numbers), 6)
        self.assertEqual(numbers[0], 1)
        self.assertEqual(numbers[1], 1)
        self.assertEqual(numbers[2], 3)
        self.assertEqual(numbers[3], 5)
        self.assertEqual(numbers[4], 9)
        self.assertEqual(numbers[5], 15)

    def test_sort_empty_array(self):
        """Тест сортировки пустого массива"""
        arr = []
        self.sorter.sort(arr)
        self.assertEqual(arr, [])
        self.assertEqual(self.sorter.comparisons_count, 0)

    def test_sort_single_element(self):
        """Тест сортировки массива из одного элемента"""
        arr = [5]
        self.sorter.sort(arr)
        self.assertEqual(arr, [5])

    def test_sort_small_arrays(self):
        """Тест сортировки маленьких массивов"""
        test_cases = [
            ([2, 1], [1, 2]),
            ([3, 1, 2], [1, 2, 3]),
            ([4, 2, 3, 1], [1, 2, 3, 4]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ]

        for input_arr, expected in test_cases:
            with self.subTest(input=input_arr):
                arr = input_arr.copy()
                self.sorter.sort(arr)
                self.assertEqual(arr, expected,
                                 f"Ошибка для {input_arr}. Получено: {arr}")


    def test_sort_with_duplicates_small(self):
        """Тест сортировки с повторяющимися элементами (маленький массив)"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]

        self.sorter.sort(arr)
        self.assertEqual(arr, expected)

    def test_sort_already_sorted(self):
        """Тест сортировки уже отсортированного массива"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        arr_copy = arr.copy()

        self.sorter.sort(arr)
        self.assertEqual(arr, arr_copy)

    def test_sort_reverse_sorted(self):
        """Тест сортировки массива в обратном порядке"""
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.sorter.sort(arr)
        self.assertEqual(arr, expected)

    def test_sort_strings(self):
        """Тест сортировки строк"""
        arr = ["яблоко", "банан", "апельсин", "киви"]
        expected = sorted(arr.copy())

        self.sorter.sort(arr)
        self.assertEqual(arr, expected)

    def test_sort_with_key(self):
        """Тест сортировки с ключевой функцией"""
        arr = ["aaa", "bb", "c"]
        expected = sorted(arr.copy(), key=len)

        self.sorter.sort(arr, key=len)
        self.assertEqual(arr, expected)

    def test_sort_reverse(self):
        """Тест обратной сортировки"""
        arr = [1, 3, 2, 5, 4]
        expected = sorted(arr.copy(), reverse=True)

        self.sorter.sort(arr, reverse=True)
        self.assertEqual(arr, expected)

    def test_sort_students(self):
        """Тест сортировки студентов по имени"""
        students = self.factory.create_sample_students()
        students_copy = students.copy()

        self.sorter.sort(students_copy, key=lambda s: s.name)

        # Проверяем сортировку
        for i in range(len(students_copy) - 1):
            self.assertLessEqual(students_copy[i].name, students_copy[i + 1].name)

    def test_sort_students_by_gpa(self):
        """Тест сортировки студентов по GPA"""
        students = self.factory.create_sample_students()
        students_copy = students.copy()

        self.sorter.sort(students_copy, key=lambda s: s.gpa, reverse=True)

        # Проверяем сортировку по убыванию GPA
        for i in range(len(students_copy) - 1):
            self.assertGreaterEqual(students_copy[i].gpa, students_copy[i + 1].gpa)

    def test_sort_students_by_age(self):
        """Тест сортировки студентов по возрасту"""
        students = self.factory.create_sample_students()
        students_copy = students.copy()

        self.sorter.sort(students_copy, key=lambda s: s.age)

        # Проверяем сортировку по возрасту
        for i in range(len(students_copy) - 1):
            self.assertLessEqual(students_copy[i].age, students_copy[i + 1].age)

    def test_get_stats(self):
        """Тест получения статистики"""
        arr = [5, 3, 4, 1, 2]
        self.sorter.sort(arr)

        stats = self.sorter.get_stats()
        self.assertEqual(stats['algorithm'], 'Smoothsort')
        self.assertGreater(stats['comparisons'], 0)
        self.assertGreater(stats['swaps'], 0)

        # Проверяем корректность сортировки
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_split_tree(self):
        """Тест метода разделения дерева"""
        # Инициализируем числа Леонардо
        self.sorter._build_leonardo_numbers(20)

        # Для дерева порядка 4 (размер 9)
        result = self.sorter._split_tree(10, 4)
        right_root, right_order, left_root, left_order = result

        self.assertEqual(right_root, 9)  # root - 1
        self.assertEqual(right_order, 2)  # order - 2
        self.assertEqual(left_root, 6)  # right_root - leo[right_order] = 9 - 3
        self.assertEqual(left_order, 3)  # order - 1

        # Граничный случай
        result = self.sorter._split_tree(0, 1)
        self.assertEqual(result[0], None)  # Для order < 2 возвращаем None


if __name__ == "__main__":
    unittest.main()