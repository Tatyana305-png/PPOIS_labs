import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.AudioModels.AudioMetadata import AudioMetadata


class TestAudioMetadata(unittest.TestCase):

    def setUp(self):
        """Настройка тестового окружения перед каждым тестом"""
        self.metadata = AudioMetadata()

    def test_initial_state(self):
        """Тест начального состояния объекта AudioMetadata"""
        self.assertEqual(self.metadata.id3_tags, {})
        self.assertIsNone(self.metadata.artwork)
        self.assertEqual(self.metadata.copyright, "")
        self.assertEqual(self.metadata.encoder, "")
        self.assertEqual(self.metadata.comments, "")

    def test_add_id3_tag_valid(self):
        """Тест добавления корректных ID3 тегов"""
        # Добавление одного тега
        self.metadata.add_id3_tag("artist", "Test Artist")
        self.assertEqual(self.metadata.id3_tags["artist"], "Test Artist")
        self.assertEqual(len(self.metadata.id3_tags), 1)

        # Добавление нескольких тегов
        self.metadata.add_id3_tag("title", "Test Song")
        self.metadata.add_id3_tag("album", "Test Album")

        self.assertEqual(len(self.metadata.id3_tags), 3)
        self.assertEqual(self.metadata.id3_tags["title"], "Test Song")
        self.assertEqual(self.metadata.id3_tags["album"], "Test Album")

    def test_add_id3_tag_empty_key(self):
        """Тест добавления ID3 тега с пустым ключом"""
        self.metadata.add_id3_tag("", "Some Value")
        self.assertEqual(len(self.metadata.id3_tags), 0)

    def test_add_id3_tag_empty_value(self):
        """Тест добавления ID3 тега с пустым значением"""
        self.metadata.add_id3_tag("artist", "")
        self.assertEqual(len(self.metadata.id3_tags), 0)

    def test_add_id3_tag_none_values(self):
        """Тест добавления ID3 тега с None значениями"""
        self.metadata.add_id3_tag(None, "Value")
        self.assertEqual(len(self.metadata.id3_tags), 0)

        self.metadata.add_id3_tag("key", None)
        self.assertEqual(len(self.metadata.id3_tags), 0)

    def test_add_id3_tag_duplicate_key(self):
        """Тест добавления ID3 тега с существующим ключом (перезапись)"""
        self.metadata.add_id3_tag("artist", "First Artist")
        self.assertEqual(self.metadata.id3_tags["artist"], "First Artist")

        self.metadata.add_id3_tag("artist", "Second Artist")
        self.assertEqual(self.metadata.id3_tags["artist"], "Second Artist")
        self.assertEqual(len(self.metadata.id3_tags), 1)

    def test_get_id3_tag_existing(self):
        """Тест получения существующего ID3 тега"""
        self.metadata.add_id3_tag("genre", "Rock")
        self.metadata.add_id3_tag("year", "2023")

        self.assertEqual(self.metadata.get_id3_tag("genre"), "Rock")
        self.assertEqual(self.metadata.get_id3_tag("year"), "2023")

    def test_get_id3_tag_nonexistent(self):
        """Тест получения несуществующего ID3 тега"""
        self.assertEqual(self.metadata.get_id3_tag("nonexistent"), "")
        self.assertEqual(self.metadata.get_id3_tag(""), "")

    def test_has_artwork(self):
        """Тест проверки наличия обложки"""
        # Изначально обложки нет
        self.assertFalse(self.metadata.has_artwork())

        # Устанавливаем обложку
        self.metadata.artwork = b"fake_image_data"
        self.assertTrue(self.metadata.has_artwork())

        # Устанавливаем обложку в None
        self.metadata.artwork = None
        self.assertFalse(self.metadata.has_artwork())

    def test_has_artwork_with_different_values(self):
        """Тест проверки наличия обложки с различными значениями"""
        # Пустая строка
        self.metadata.artwork = ""
        self.assertTrue(self.metadata.has_artwork())

        # Пустые байты
        self.metadata.artwork = b""
        self.assertTrue(self.metadata.has_artwork())

        # Число
        self.metadata.artwork = 123
        self.assertTrue(self.metadata.has_artwork())

        # Список
        self.metadata.artwork = [1, 2, 3]
        self.assertTrue(self.metadata.has_artwork())

    def test_get_metadata_summary_empty(self):
        """Тест получения сводки метаданных для пустого объекта"""
        summary = self.metadata.get_metadata_summary()

        expected = {
            'total_id3_tags': 0,
            'has_artwork': False,
            'has_copyright': False,
            'encoder': ""
        }
        self.assertEqual(summary, expected)

    def test_get_metadata_summary_with_data(self):
        """Тест получения сводки метаданных для заполненного объекта"""
        # Заполняем метаданные
        self.metadata.add_id3_tag("artist", "Test Artist")
        self.metadata.add_id3_tag("title", "Test Song")
        self.metadata.artwork = b"image_data"
        self.metadata.copyright = "© 2023"
        self.metadata.encoder = "LAME 3.100"
        self.metadata.comments = "Great song!"

        summary = self.metadata.get_metadata_summary()

        expected = {
            'total_id3_tags': 2,
            'has_artwork': True,
            'has_copyright': True,
            'encoder': "LAME 3.100"
        }
        self.assertEqual(summary, expected)

    def test_get_metadata_summary_partial_data(self):
        """Тест получения сводки метаданных с частичными данными"""
        self.metadata.add_id3_tag("genre", "Pop")
        self.metadata.encoder = "Custom Encoder"

        summary = self.metadata.get_metadata_summary()

        expected = {
            'total_id3_tags': 1,
            'has_artwork': False,
            'has_copyright': False,
            'encoder': "Custom Encoder"
        }
        self.assertEqual(summary, expected)

    def test_clear_id3_tags_empty(self):
        """Тест очистки пустого списка ID3 тегов"""
        self.metadata.clear_id3_tags()
        self.assertEqual(self.metadata.id3_tags, {})
        self.assertEqual(len(self.metadata.id3_tags), 0)

    def test_clear_id3_tags_with_data(self):
        """Тест очистки заполненного списка ID3 тегов"""
        # Добавляем теги
        self.metadata.add_id3_tag("artist", "Artist")
        self.metadata.add_id3_tag("title", "Title")
        self.metadata.add_id3_tag("album", "Album")

        self.assertEqual(len(self.metadata.id3_tags), 3)

        # Очищаем
        self.metadata.clear_id3_tags()

        self.assertEqual(self.metadata.id3_tags, {})
        self.assertEqual(len(self.metadata.id3_tags), 0)

    def test_clear_id3_tags_preserves_other_fields(self):
        """Тест, что очистка ID3 тегов не затрагивает другие поля"""
        # Устанавливаем все поля
        self.metadata.add_id3_tag("artist", "Artist")
        self.metadata.artwork = b"image_data"
        self.metadata.copyright = "Copyright"
        self.metadata.encoder = "Encoder"
        self.metadata.comments = "Comments"

        # Очищаем только ID3 теги
        self.metadata.clear_id3_tags()

        # Проверяем, что другие поля сохранились
        self.assertEqual(self.metadata.id3_tags, {})
        self.assertEqual(self.metadata.artwork, b"image_data")
        self.assertEqual(self.metadata.copyright, "Copyright")
        self.assertEqual(self.metadata.encoder, "Encoder")
        self.assertEqual(self.metadata.comments, "Comments")

    def test_multiple_operations_sequence(self):
        """Тест последовательности различных операций"""
        # Начальное состояние
        self.assertEqual(len(self.metadata.id3_tags), 0)

        # Добавляем теги
        self.metadata.add_id3_tag("track", "1")
        self.metadata.add_id3_tag("disc", "1")
        self.assertEqual(len(self.metadata.id3_tags), 2)

        # Получаем теги
        self.assertEqual(self.metadata.get_id3_tag("track"), "1")
        self.assertEqual(self.metadata.get_id3_tag("disc"), "1")

        # Обновляем тег
        self.metadata.add_id3_tag("track", "2")
        self.assertEqual(self.metadata.get_id3_tag("track"), "2")

        # Получаем сводку
        summary = self.metadata.get_metadata_summary()
        self.assertEqual(summary['total_id3_tags'], 2)

        # Очищаем теги
        self.metadata.clear_id3_tags()
        self.assertEqual(len(self.metadata.id3_tags), 0)

        # Проверяем получение несуществующего тега после очистки
        self.assertEqual(self.metadata.get_id3_tag("track"), "")

    def test_id3_tags_case_sensitivity(self):
        """Тест чувствительности к регистру в ID3 тегах"""
        self.metadata.add_id3_tag("Artist", "Artist1")
        self.metadata.add_id3_tag("artist", "Artist2")
        self.metadata.add_id3_tag("ARTIST", "Artist3")

        # Должны быть три разных тега из-за разного регистра
        self.assertEqual(len(self.metadata.id3_tags), 3)
        self.assertEqual(self.metadata.get_id3_tag("Artist"), "Artist1")
        self.assertEqual(self.metadata.get_id3_tag("artist"), "Artist2")
        self.assertEqual(self.metadata.get_id3_tag("ARTIST"), "Artist3")

    def test_special_characters_in_id3_tags(self):
        """Тест специальных символов в ID3 тегах"""
        special_key = "key-with-dash"
        special_value = "Value with spaces & symbols!@#$%"

        self.metadata.add_id3_tag(special_key, special_value)
        self.assertEqual(self.metadata.get_id3_tag(special_key), special_value)

        # Юникод символы
        unicode_key = "исполнитель"
        unicode_value = "Песня с русскими буквами"

        self.metadata.add_id3_tag(unicode_key, unicode_value)
        self.assertEqual(self.metadata.get_id3_tag(unicode_key), unicode_value)

    def test_metadata_summary_immutability(self):
        """Тест, что возвращаемая сводка не связана с оригинальным объектом"""
        summary = self.metadata.get_metadata_summary()
        original_total = summary['total_id3_tags']

        # Изменяем оригинальный объект
        self.metadata.add_id3_tag("new", "tag")

        # Сводка не должна измениться
        self.assertEqual(summary['total_id3_tags'], original_total)

        # Новая сводка должна отражать изменения
        new_summary = self.metadata.get_metadata_summary()
        self.assertEqual(new_summary['total_id3_tags'], original_total + 1)


if __name__ == '__main__':
    unittest.main()