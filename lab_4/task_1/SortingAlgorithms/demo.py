from StudentFactory import StudentFactory
from Smoothsort import Smoothsort
from PancakeSort import PancakeSort


class SortingDemo:
    """Класс для демонстрации работы алгоритмов сортировки"""

    def __init__(self):
        """Инициализация демонстрации"""
        self._student_factory = StudentFactory()
        self._smoothsort = Smoothsort()
        self._pancake_sort = PancakeSort()
        self._separator_length = 70

    def run_full_demo(self):
        """Запуск полной демонстрации"""
        self._print_header("ПОЛНАЯ ДЕМОНСТРАЦИЯ АЛГОРИТМОВ СОРТИРОВКИ")

        self._demo_basic_types()
        self._demo_student_sorting()

        self._print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")

    def _demo_basic_types(self):
        """Демонстрация сортировки базовых типов данных"""
        self._print_header("СОРТИРОВКА БАЗОВЫХ ТИПОВ ДАННЫХ")

        # 1. Числа
        print("\n1. СОРТИРОВКА ЧИСЕЛ:")
        numbers = [64, 34, 25, 12, 22, 11, 90, 5, 77, 43]
        print(f"Исходный массив: {numbers}")

        numbers_smooth = numbers.copy()
        self._smoothsort.sort(numbers_smooth)
        print(f"Smoothsort: {numbers_smooth}")

        numbers_pancake = numbers.copy()
        self._pancake_sort.sort(numbers_pancake)
        print(f"Pancake:    {numbers_pancake}")

        # 2. Строки
        print("\n2. СОРТИРОВКА СТРОК:")
        strings = ["яблоко", "банан", "апельсин", "киви", "манго", "груша"]
        print(f"Исходный массив: {strings}")

        strings_smooth = strings.copy()
        self._smoothsort.sort(strings_smooth)
        print(f"Smoothsort: {strings_smooth}")

        strings_pancake = strings.copy()
        self._pancake_sort.sort(strings_pancake)
        print(f"Pancake:    {strings_pancake}")

        # 3. Сортировка с параметрами
        print("\n3. СОРТИРОВКА С ПАРАМЕТРАМИ:")
        words = ["кот", "собака", "слон", "тигр", "жираф", "мышь"]
        print(f"Исходный массив: {words}")

        # Сортировка по длине
        words_by_length = words.copy()
        self._smoothsort.sort(words_by_length, key=len)
        print(f"Smoothsort по длине: {words_by_length}")

        # Обратная сортировка
        numbers_reverse = [1, 3, 2, 5, 4]
        numbers_rev_copy = numbers_reverse.copy()
        self._pancake_sort.sort(numbers_rev_copy, reverse=True)
        print(f"Pancake обратная сортировка: {numbers_rev_copy}")

    def _demo_student_sorting(self):
        """Демонстрация сортировки объектов класса Student"""
        self._print_header("СОРТИРОВКА ОБЪЕКТОВ КЛАССА STUDENT")

        students = self._student_factory.create_sample_students()

        print("\nИсходный список студентов:")
        for i, student in enumerate(students, 1):
            print(f"  {i}. {student}")

        # Сортировка по разным критериям
        print("\n1. СОРТИРОВКА ПО ИМЕНИ:")
        students_by_name = students.copy()
        self._smoothsort.sort(students_by_name, key=lambda s: s.name)
        for student in students_by_name:
            print(f"  {student}")

        print("\n2. СОРТИРОВКА ПО ВОЗРАСТУ:")
        students_by_age = students.copy()
        self._pancake_sort.sort(students_by_age, key=lambda s: s.age)
        for student in students_by_age:
            print(f"  {student}")

        print("\n3. СОРТИРОВКА ПО GPA (ПО УБЫВАНИЮ):")
        students_by_gpa = students.copy()
        self._smoothsort.sort(students_by_gpa, key=lambda s: s.gpa, reverse=True)
        for student in students_by_gpa:
            print(f"  {student}")


    def _print_header(self, text: str):
        """Вывод заголовка"""
        print("\n" + "=" * self._separator_length)
        print(text)
        print("=" * self._separator_length)


def main():
    """Запуск демонстрации"""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 70)

    try:
        demo = SortingDemo()
        demo.run_full_demo()

    except Exception as e:
        print(f"\nОшибка при выполнении: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
