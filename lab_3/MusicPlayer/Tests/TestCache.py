import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Cache import Cache


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = Cache(max_size=3)

    def test_cache_initialization(self):
        """Тест инициализации кэша"""
        self.assertEqual(self.cache.max_size, 3)
        self.assertEqual(len(self.cache.cache), 0)
        self.assertEqual(len(self.cache.access_times), 0)

    def test_set_and_get(self):
        """Тест добавления и получения из кэша"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", 123)
        self.cache.set("key3", [1, 2, 3])

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), 123)
        self.assertEqual(self.cache.get("key3"), [1, 2, 3])

    def test_get_nonexistent(self):
        """Тест получения несуществующего ключа"""
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_cache_eviction(self):
        """Тест вытеснения старых записей при переполнении"""
        # Заполняем кэш
        self.cache.set("key1", "value1")
        time.sleep(0.01)  # Небольшая задержка для разного времени доступа
        self.cache.set("key2", "value2")
        time.sleep(0.01)
        self.cache.set("key3", "value3")

        # Все ключи должны быть в кэше
        self.assertIsNotNone(self.cache.get("key1"))
        self.assertIsNotNone(self.cache.get("key2"))
        self.assertIsNotNone(self.cache.get("key3"))

        # Добавляем четвертый ключ - должен вытеснить самый старый (key1)
        self.cache.set("key4", "value4")

        # key1 должен быть вытеснен
        self.assertIsNone(self.cache.get("key1"))
        # Остальные ключи должны остаться
        self.assertIsNotNone(self.cache.get("key2"))
        self.assertIsNotNone(self.cache.get("key3"))
        self.assertIsNotNone(self.cache.get("key4"))

    def test_access_time_update(self):
        """Тест обновления времени доступа"""
        self.cache.set("key1", "value1")
        initial_time = self.cache.access_times["key1"]

        time.sleep(0.01)
        # При получении время доступа должно обновиться
        self.cache.get("key1")
        updated_time = self.cache.access_times["key1"]

        self.assertGreater(updated_time, initial_time)

    def test_cache_size_limit(self):
        """Тест ограничения размера кэша"""
        cache_small = Cache(max_size=2)

        cache_small.set("key1", "value1")
        cache_small.set("key2", "value2")
        cache_small.set("key3", "value3")  # Должен вытеснить key1

        self.assertEqual(len(cache_small.cache), 2)
        self.assertIsNone(cache_small.get("key1"))
        self.assertIsNotNone(cache_small.get("key2"))
        self.assertIsNotNone(cache_small.get("key3"))

    def test_overwrite_existing_key(self):
        """Тест перезаписи существующего ключа"""
        self.cache.set("key1", "old_value")
        self.cache.set("key1", "new_value")

        self.assertEqual(self.cache.get("key1"), "new_value")
        self.assertEqual(len(self.cache.cache), 1)

    def test_evict_oldest_with_access_pattern(self):
        """Тест вытеснения с учетом паттерна доступа"""
        self.cache.set("key1", "value1")
        time.sleep(0.01)
        self.cache.set("key2", "value2")
        time.sleep(0.01)
        self.cache.set("key3", "value3")

        # Доступ к key1 делает его "моложе"
        self.cache.get("key1")

        # Добавляем новый ключ - должен вытеснить key2 (самый старый из неиспользованных)
        self.cache.set("key4", "value4")

        self.assertIsNone(self.cache.get("key2"))  # key2 вытеснен
        self.assertIsNotNone(self.cache.get("key1"))  # key1 остался
        self.assertIsNotNone(self.cache.get("key3"))  # key3 остался
        self.assertIsNotNone(self.cache.get("key4"))  # key4 добавлен


if __name__ == '__main__':
    unittest.main()