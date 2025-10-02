import sys
import os

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unordered_multiset import UnorderedMultiset


def main():
    """Демонстрация работы класса с новыми функциями"""
    print("Демонстрация работы Неориентированного мультимножества")
    print("=" * 60)

    # Пример 1: Простое множество
    print("1. Простое множество:")
    ms1 = UnorderedMultiset("{a, b, c, a, b}")
    print(f"   Множество: {ms1}")
    print(f"   Количество 'a': {ms1.count('a')}")
    print(f"   Количество 'b': {ms1.count('b')}")
    print(f"   Общий размер: {len(ms1)}")
    print(f"   Уникальных элементов: {ms1.unique_count()}")
    print(f"   Пустое множество: {ms1.is_empty()}")
    print()

    # Пример 2: Вложенные множества
    print("2. Вложенные множества:")
    ms2 = UnorderedMultiset("{a, {b, c}, {}, {a, {x, y}}}")
    print(f"   Множество: {ms2}")
    print(f"   Пустое множество: {ms2.is_empty()}")
    print()

    # Пример 3: Базовые операции
    print("3. Базовые операции над множествами:")
    set_a = UnorderedMultiset("{a, a, b, c}")
    set_b = UnorderedMultiset("{a, b, b, d}")

    print(f"   Множество A: {set_a}")
    print(f"   Множество B: {set_b}")
    print(f"   A + B (объединение): {set_a + set_b}")
    print(f"   A - B (разность): {set_a - set_b}")
    print(f"   A * B (пересечение): {set_a * set_b}")
    print()

    # Пример 4: Проверка принадлежности
    print("4. Проверка принадлежности:")
    test_set = UnorderedMultiset("{a, b, c, {x, y}}")
    print(f"   Множество: {test_set}")
    print(f"   'a' в множестве: {'a' in test_set}")
    print(f"   'z' в множестве: {'z' in test_set}")

    # Проверка вложенного множества
    nested = UnorderedMultiset("{x, y}")
    print(f"   {{x, y}} в множестве: {nested in test_set}")
    print()

    # Пример 5: Операторы +=, -=, *=
    print("5. Операторы присваивания:")
    ms3 = UnorderedMultiset("{x, y, z}")
    ms4 = UnorderedMultiset("{y, z, w}")

    print(f"   Исходное множество: {ms3}")
    ms3 += ms4
    print(f"   После += {ms4}: {ms3}")

    ms3 -= UnorderedMultiset("{y, z}")
    print(f"   После -= {{y, z}}: {ms3}")

    ms5 = UnorderedMultiset("{a, a, b, c}")
    ms6 = UnorderedMultiset("{a, b, b}")
    ms5 *= ms6
    print(f"   После *= {{a, b, b}}: {ms5}")
    print()

    # Пример 6: Булеан (множество всех подмножеств)
    print("6. Булеан множества:")
    simple_ms = UnorderedMultiset("{a, b}")
    print(f"   Исходное множество: {simple_ms}")

    power_set = simple_ms.power_set()
    print(f"   Все подмножества ({len(power_set)} шт.):")
    for i, subset in enumerate(power_set, 1):
        print(f"      {i:2d}. {subset}")
    print()

    # Пример 7: Работа с пустым множеством
    print("7. Работа с пустым множеством:")
    empty_ms = UnorderedMultiset()
    print(f"   Пустое множество: {empty_ms}")
    print(f"   is_empty(): {empty_ms.is_empty()}")
    print(f"   Размер: {len(empty_ms)}")

    # Добавление в пустое множество
    empty_ms.add("new_element")
    print(f"   После добавления элемента: {empty_ms}")
    print(f"   is_empty(): {empty_ms.is_empty()}")
    print()

    # Пример 8: Сложные вложенные структуры
    print("8. Сложные вложенные структуры:")
    complex_ms = UnorderedMultiset("{a, {b, {c, d}}, {e, f}, {}}")
    print(f"   Сложное множество: {complex_ms}")
    print(f"   Размер: {len(complex_ms)}")

    # Проверка вложенности
    nested1 = UnorderedMultiset("{b, {c, d}}")
    nested2 = UnorderedMultiset("{e, f}")
    empty_nested = UnorderedMultiset("{}")

    print(f"   {{b, {{c, d}}}} в множестве: {nested1 in complex_ms}")
    print(f"   {{e, f}} в множестве: {nested2 in complex_ms}")
    print(f"   {{}} в множестве: {empty_nested in complex_ms}")
    print()

    # Пример 9: Комплексные операции
    print("9. Комплексные операции:")
    base_set = UnorderedMultiset("{1, 2, 2, 3}")
    operation_set = UnorderedMultiset("{2, 3, 4}")

    print(f"   Базовое множество: {base_set}")
    print(f"   Операционное множество: {operation_set}")
    print(f"   Объединение: {base_set + operation_set}")
    print(f"   Разность: {base_set - operation_set}")
    print(f"   Пересечение: {base_set * operation_set}")

    # Цепочка операций
    result = (base_set + operation_set) * UnorderedMultiset("{2, 4}")
    print(f"   (A + B) * {{2, 4}}: {result}")


if __name__ == "__main__":
    main()
