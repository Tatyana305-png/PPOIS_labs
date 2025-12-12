from StudentFactory import StudentFactory
from Smoothsort import Smoothsort
from PancakeSort import PancakeSort


def run_comprehensive_tests():
    """Запуск комплексных тестов для проверки алгоритмов"""
    print("=" * 60)
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 60)

    # Инициализация алгоритмов
    smoothsort = Smoothsort()
    pancake_sort = PancakeSort()

    # Тест 1: Базовые случаи сортировки чисел
    print("\n1. ТЕСТ БАЗОВЫХ СЛУЧАЕВ СОРТИРОВКИ ЧИСЕЛ:")
    print("-" * 50)

    test_cases = [
        ("Пустой массив", []),
        ("Один элемент", [1]),
        ("Два элемента (уже отсортированы)", [1, 2]),
        ("Два элемента (не отсортированы)", [2, 1]),
        ("Три элемента", [3, 1, 2]),
        ("Пять элементов в обратном порядке", [5, 4, 3, 2, 1]),
        ("Пять элементов в случайном порядке", [5, 1, 4, 2, 3]),
        ("Десять элементов", [64, 34, 25, 12, 22, 11, 90, 5, 77, 43]),
        ("С повторяющимися элементами", [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]),
        ("Уже отсортированный массив", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ]

    all_tests_passed = True

    for test_name, test_array in test_cases:
        print(f"\n{test_name}: {test_array}")

        # Ожидаемый результат
        expected = sorted(test_array.copy())

        # Тестируем Smoothsort
        arr_smooth = test_array.copy()
        smoothsort.sort(arr_smooth)
        smooth_ok = arr_smooth == expected

        # Тестируем Pancake Sort
        arr_pancake = test_array.copy()
        pancake_sort.sort(arr_pancake)
        pancake_ok = arr_pancake == expected

        print(f"  Smoothsort: {'✓' if smooth_ok else '✗'} {arr_smooth}")
        print(f"  Pancake:    {'✓' if pancake_ok else '✗'} {arr_pancake}")

        if not smooth_ok or not pancake_ok:
            print(f"    Ожидалось: {expected}")
            all_tests_passed = False

    # Тест 2: Сортировка строк
    print("\n\n2. ТЕСТ СОРТИРОВКИ СТРОК:")
    print("-" * 50)

    string_test_cases = [
        ("Простой список", ["яблоко", "банан", "апельсин", "киви"]),
        ("Слова разной длины", ["кот", "собака", "слон", "тигр", "жираф", "мышь"]),
        ("С повторениями", ["яблоко", "банан", "яблоко", "киви", "банан"]),
    ]

    for test_name, test_array in string_test_cases:
        print(f"\n{test_name}: {test_array}")

        expected = sorted(test_array.copy())

        arr_smooth = test_array.copy()
        smoothsort.sort(arr_smooth)
        smooth_ok = arr_smooth == expected

        arr_pancake = test_array.copy()
        pancake_sort.sort(arr_pancake)
        pancake_ok = arr_pancake == expected

        print(f"  Smoothsort: {'✓' if smooth_ok else '✗'} {arr_smooth}")
        print(f"  Pancake:    {'✓' if pancake_ok else '✗'} {arr_pancake}")

        if not smooth_ok or not pancake_ok:
            all_tests_passed = False

    # Тест 3: Сортировка с параметрами key и reverse
    print("\n\n3. ТЕСТ СОРТИРОВКИ С ПАРАМЕТРАМИ:")
    print("-" * 50)

    words = ["кот", "собака", "слон", "тигр", "жираф", "мышь"]
    print(f"Исходный массив: {words}")

    # Сортировка по длине строки
    words_smooth = words.copy()
    smoothsort.sort(words_smooth, key=len)
    expected_by_length = sorted(words.copy(), key=len)
    print(f"\n  Smoothsort по длине: {words_smooth}")
    print(f"  Ожидалось: {expected_by_length}")
    print(f"  Результат: {'✓' if words_smooth == expected_by_length else '✗'}")

    # Обратная сортировка
    numbers = [1, 3, 2, 5, 4]
    numbers_pancake = numbers.copy()
    pancake_sort.sort(numbers_pancake, reverse=True)
    expected_reverse = sorted(numbers.copy(), reverse=True)
    print(f"\n  Pancake обратная сортировка: {numbers_pancake}")
    print(f"  Ожидалось: {expected_reverse}")
    print(f"  Результат: {'✓' if numbers_pancake == expected_reverse else '✗'}")

    # Тест 4: Сортировка студентов
    print("\n\n4. ТЕСТ СОРТИРОВКИ СТУДЕНТОВ:")
    print("-" * 50)

    factory = StudentFactory()
    students = factory.create_sample_students()

    print("Исходный список студентов:")
    for i, student in enumerate(students, 1):
        print(f"  {i}. {student}")

    # Сортировка по имени
    print("\nСортировка по имени:")
    students_by_name_smooth = students.copy()
    smoothsort.sort(students_by_name_smooth, key=lambda s: s.name)

    students_by_name_pancake = students.copy()
    pancake_sort.sort(students_by_name_pancake, key=lambda s: s.name)

    smooth_names = [s.name for s in students_by_name_smooth]
    pancake_names = [s.name for s in students_by_name_pancake]

    print(f"  Smoothsort: {smooth_names}")
    print(f"  Pancake:    {pancake_names}")

    # Проверяем, что оба отсортированы правильно
    smooth_sorted = all(smooth_names[i] <= smooth_names[i + 1]
                        for i in range(len(smooth_names) - 1))
    pancake_sorted = all(pancake_names[i] <= pancake_names[i + 1]
                         for i in range(len(pancake_names) - 1))

    print(f"  Smoothsort {'✓' if smooth_sorted else '✗'} отсортирован")
    print(f"  Pancake    {'✓' if pancake_sorted else '✗'} отсортирован")

    if not smooth_sorted or not pancake_sorted:
        all_tests_passed = False

    # Сортировка по GPA (по убыванию)
    print("\nСортировка по GPA (по убыванию):")
    students_by_gpa_smooth = students.copy()
    smoothsort.sort(students_by_gpa_smooth, key=lambda s: s.gpa, reverse=True)

    smooth_gpas = [s.gpa for s in students_by_gpa_smooth]
    gpa_sorted = all(smooth_gpas[i] >= smooth_gpas[i + 1]
                     for i in range(len(smooth_gpas) - 1))
    print(f"  Smoothsort GPA: {smooth_gpas} {'✓' if gpa_sorted else '✗'}")

    # Итоги тестирования
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("ОБНАРУЖЕНЫ ОШИБКИ В АЛГОРИТМАХ!")
    print("=" * 60)

    return all_tests_passed


def main():
    """Основная функция программы"""
    print("=" * 70)
    print("ПРОГРАММА ДЛЯ ТЕСТИРОВАНИЯ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 70)

    try:
        # Запускаем комплексные тесты
        tests_passed = run_comprehensive_tests()

        if tests_passed:
            print("\n\n" + "=" * 70)
            print("ВСЕ АЛГОРИТМЫ РАБОТАЮТ КОРРЕКТНО!")
            print("Теперь можно запустить демонстрацию.")
            print("=" * 70)
        else:
            print("\n\n" + "=" * 70)
            print("ЕСТЬ ПРОБЛЕМЫ С АЛГОРИТМАМИ СОРТИРОВКИ.")
            print("=" * 70)
            return 1

    except Exception as e:
        print(f"\nОшибка при выполнении программы: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())