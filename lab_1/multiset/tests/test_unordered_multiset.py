import unittest
import sys
import os

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from unordered_multiset import UnorderedMultiset


class TestUnorderedMultiset(unittest.TestCase):

    def test_empty_initialization(self):
        """Тест создания пустого множества"""
        ms = UnorderedMultiset()
        self.assertEqual(len(ms), 0)
        self.assertEqual(str(ms), "{}")

    def test_string_initialization_simple(self):
        """Тест создания из простой строки"""
        ms = UnorderedMultiset("{a, b, c}")
        self.assertEqual(len(ms), 3)
        self.assertEqual(ms.count("a"), 1)
        self.assertEqual(ms.count("b"), 1)
        self.assertEqual(ms.count("c"), 1)

    def test_string_initialization_duplicates(self):
        """Тест создания с дубликатами"""
        ms = UnorderedMultiset("{a, a, b}")
        self.assertEqual(len(ms), 3)
        self.assertEqual(ms.count("a"), 2)
        self.assertEqual(ms.count("b"), 1)

    def test_nested_sets(self):
        """Тест вложенных множеств"""
        ms = UnorderedMultiset("{a, {b, c}, {}}")
        self.assertEqual(len(ms), 3)

        # Проверяем наличие вложенного множества
        nested = UnorderedMultiset("{b, c}")
        self.assertEqual(ms.count(nested), 1)

    def test_complex_nested(self):
        """Тест сложного вложенного множества"""
        ms = UnorderedMultiset("{a, a, c, {a, b, b}, {}, {a, {c, c}}}")
        self.assertTrue(len(ms) > 0)

        # Проверяем простые элементы
        self.assertEqual(ms.count("a"), 2)
        self.assertEqual(ms.count("c"), 1)

        # Проверяем вложенные множества
        nested1 = UnorderedMultiset("{a, b, b}")
        nested2 = UnorderedMultiset("{}")
        nested3 = UnorderedMultiset("{a, {c, c}}")

        self.assertEqual(ms.count(nested1), 1)
        self.assertEqual(ms.count(nested2), 1)
        self.assertEqual(ms.count(nested3), 1)

    def test_add_remove(self):
        """Тест добавления и удаления элементов"""
        ms = UnorderedMultiset()
        ms.add("a")
        ms.add("a")
        ms.add("b")

        self.assertEqual(ms.count("a"), 2)
        self.assertEqual(ms.count("b"), 1)

        ms.remove("a")
        self.assertEqual(ms.count("a"), 1)

        ms.remove("a")
        self.assertEqual(ms.count("a"), 0)

    def test_contains(self):
        """Тест оператора in"""
        ms = UnorderedMultiset("{a, b, c}")
        self.assertTrue("a" in ms)
        self.assertTrue("b" in ms)
        self.assertFalse("z" in ms)

    def test_union(self):
        """Тест объединения множеств"""
        ms1 = UnorderedMultiset("{a, b}")
        ms2 = UnorderedMultiset("{b, c}")

        result = ms1 + ms2
        self.assertEqual(result.count("a"), 1)
        self.assertEqual(result.count("b"), 2)
        self.assertEqual(result.count("c"), 1)

    def test_difference(self):
        """Тест разности множеств"""
        ms1 = UnorderedMultiset("{a, a, b, c}")
        ms2 = UnorderedMultiset("{a, b}")

        result = ms1 - ms2
        self.assertEqual(result.count("a"), 1)
        self.assertEqual(result.count("b"), 0)
        self.assertEqual(result.count("c"), 1)

    def test_equality(self):
        """Тест равенства множеств"""
        ms1 = UnorderedMultiset("{a, b, c}")
        ms2 = UnorderedMultiset("{a, b, c}")
        ms3 = UnorderedMultiset("{a, a, b}")

        self.assertEqual(ms1, ms2)
        self.assertNotEqual(ms1, ms3)


    def test_is_empty(self):
        """Тест проверки на пустое множество"""
        empty_ms = UnorderedMultiset()
        self.assertTrue(empty_ms.is_empty())

        non_empty_ms = UnorderedMultiset("{a}")
        self.assertFalse(non_empty_ms.is_empty())

        # После добавления элемента
        empty_ms.add("test")
        self.assertFalse(empty_ms.is_empty())

        # После удаления всех элементов
        non_empty_ms.remove("a")
        self.assertTrue(non_empty_ms.is_empty())

    def test_iadd_operator(self):
        """Тест оператора +="""
        ms1 = UnorderedMultiset("{a, b}")
        ms2 = UnorderedMultiset("{b, c}")

        original_id = id(ms1)
        ms1 += ms2

        self.assertEqual(ms1.count("a"), 1)
        self.assertEqual(ms1.count("b"), 2)
        self.assertEqual(ms1.count("c"), 1)

        # Проверка, что возвращается тот же объект (по id)
        self.assertEqual(id(ms1), original_id)

    def test_isub_operator(self):
        """Тест оператора -="""
        ms1 = UnorderedMultiset("{a, a, b, c}")
        ms2 = UnorderedMultiset("{a, b}")

        original_id = id(ms1)
        ms1 -= ms2

        self.assertEqual(ms1.count("a"), 1)
        self.assertEqual(ms1.count("b"), 0)
        self.assertEqual(ms1.count("c"), 1)

        # Проверка, что возвращается тот же объект
        self.assertEqual(id(ms1), original_id)

        # Проверка полного удаления
        ms1 -= UnorderedMultiset("{a, c}")
        self.assertEqual(ms1.count("a"), 0)
        self.assertEqual(ms1.count("c"), 0)
        self.assertTrue(ms1.is_empty())

    def test_intersection_operator(self):
        """Тест оператора * для пересечения"""
        ms1 = UnorderedMultiset("{a, a, b, c}")
        ms2 = UnorderedMultiset("{a, b, b, d}")

        result = ms1 * ms2
        self.assertEqual(result.count("a"), 1)  # min(2, 1)
        self.assertEqual(result.count("b"), 1)  # min(1, 2)
        self.assertEqual(result.count("c"), 0)
        self.assertEqual(result.count("d"), 0)

        # Пересечение с пустым множеством
        empty_ms = UnorderedMultiset()
        result2 = ms1 * empty_ms
        self.assertTrue(result2.is_empty())

    def test_imul_operator(self):
        """Тест оператора *="""
        ms1 = UnorderedMultiset("{a, a, b, c}")
        ms2 = UnorderedMultiset("{a, b, b, d}")

        original_id = id(ms1)
        ms1 *= ms2

        self.assertEqual(ms1.count("a"), 1)
        self.assertEqual(ms1.count("b"), 1)
        self.assertEqual(ms1.count("c"), 0)
        self.assertEqual(ms1.count("d"), 0)

        # Проверка, что возвращается тот же объект
        self.assertEqual(id(ms1), original_id)

    def test_power_set_basic(self):
        """Тест построения булеана для простого множества"""
        ms = UnorderedMultiset("{a, b}")
        power_set = ms.power_set()

        # Должно быть 2^2 = 4 подмножества
        self.assertEqual(len(power_set), 4)

        # Проверяем наличие конкретных подмножеств
        subsets_str = [str(subset) for subset in power_set]
        self.assertIn("{}", subsets_str)
        self.assertIn("{a}", subsets_str)
        self.assertIn("{b}", subsets_str)
        self.assertIn("{a, b}", subsets_str)

    def test_power_set_with_duplicates(self):
        """Тест построения булеана для множества с дубликатами"""
        ms = UnorderedMultiset("{a, a, b}")
        power_set = ms.power_set()

        # Для {a, a, b} должно быть 2^3 = 8 подмножеств
        self.assertEqual(len(power_set), 8)

        # Проверяем некоторые ключевые подмножества
        subsets_str = [str(subset) for subset in power_set]
        self.assertIn("{}", subsets_str)
        self.assertIn("{a}", subsets_str)
        self.assertIn("{a, a}", subsets_str)
        self.assertIn("{b}", subsets_str)
        self.assertIn("{a, b}", subsets_str)
        self.assertIn("{a, a, b}", subsets_str)

    def test_power_set_empty(self):
        """Тест построения булеана пустого множества"""
        empty_ms = UnorderedMultiset()
        power_set = empty_ms.power_set()

        # Булеан пустого множества должен содержать только пустое множество
        self.assertEqual(len(power_set), 1)
        self.assertEqual(str(power_set[0]), "{}")

    def test_compound_operations(self):
        """Тест комплексных операций"""
        ms1 = UnorderedMultiset("{1, 2, 3}")
        ms2 = UnorderedMultiset("{2, 3, 4}")
        ms3 = UnorderedMultiset("{3, 4, 5}")

        # Цепочка операций
        result = ((ms1 + ms2) * ms3) - UnorderedMultiset("{4}")
        self.assertEqual(result.count("1"), 0)
        self.assertEqual(result.count("2"), 0)
        self.assertEqual(result.count("3"), 1)
        self.assertEqual(result.count("4"), 0)
        self.assertEqual(result.count("5"), 0)

    def test_contains_nested(self):
        """Тест проверки принадлежности для вложенных множеств"""
        ms = UnorderedMultiset("{a, {b, c}, {d, {e, f}}}")

        # Проверка простых элементов
        self.assertTrue("a" in ms)

        # Проверка вложенных множеств
        nested1 = UnorderedMultiset("{b, c}")
        self.assertTrue(nested1 in ms)

        nested2 = UnorderedMultiset("{d, {e, f}}")
        self.assertTrue(nested2 in ms)

        # Проверка несуществующих элементов
        self.assertFalse("z" in ms)
        non_existent_nested = UnorderedMultiset("{x, y}")
        self.assertFalse(non_existent_nested in ms)

    def test_unique_count(self):
        """Тест подсчета уникальных элементов"""
        ms = UnorderedMultiset("{a, a, b, c, c, c}")
        self.assertEqual(ms.unique_count(), 3)  # a, b, c

        empty_ms = UnorderedMultiset()
        self.assertEqual(empty_ms.unique_count(), 0)

    def test_iadd_with_nested(self):
        """Тест += с вложенными множествами"""
        ms1 = UnorderedMultiset("{a, {x, y}}")
        ms2 = UnorderedMultiset("{b, {x, y}}")

        ms1 += ms2
        self.assertEqual(ms1.count("a"), 1)
        self.assertEqual(ms1.count("b"), 1)

        nested = UnorderedMultiset("{x, y}")
        self.assertEqual(ms1.count(nested), 2)

    def test_intersection_with_nested(self):
        """Тест пересечения с вложенными множествами"""
        ms1 = UnorderedMultiset("{a, {x, y}, {x, y}}")  # Два одинаковых вложенных
        ms2 = UnorderedMultiset("{b, {x, y}}")

        result = ms1 * ms2
        nested = UnorderedMultiset("{x, y}")
        self.assertEqual(result.count(nested), 1)  # min(2, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
