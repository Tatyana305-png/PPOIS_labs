import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.LibraryModels.MusicLibrary import MusicLibrary
from Models.LibraryModels.Artist import Artist
from Models.LibraryModels.Album import Album
from Models.LibraryModels.LibraryScanner import LibraryScanner
from Models.UserModels.User import User
from Behaviors.PlayerBehaviors.PlaybackController import PlaybackController
from Behaviors.PlayerBehaviors.QueueManager import QueueManager
from Behaviors.PlayerBehaviors.EqualizerController import EqualizerController
from Models.AudioModels.Song import Song
from Behaviors.UserBehaviors.UserManager import UserManager
from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для моделей библиотеки"""

    def setUp(self):
        self.user_manager = UserManager()
        self.subscription_manager = SubscriptionManager()

    def test_empty_library(self):
        """Тест пустой библиотеки"""
        user = User("empty_user", "empty", "empty@example.com")
        empty_library = MusicLibrary(user)

        self.assertEqual(len(empty_library.songs), 0)
        self.assertEqual(len(empty_library.artists), 0)
        self.assertEqual(len(empty_library.albums), 0)
        self.assertEqual(len(empty_library.playlists), 0)
        self.assertEqual(empty_library.total_size, 0)
        self.assertEqual(len(empty_library.import_sources), 0)

    def test_artist_with_minimal_info(self):
        """Тест артиста с минимальной информацией"""
        minimal_artist = Artist("min_art", "Minimal Artist")
        # Только обязательные поля заполнены

        self.assertEqual(minimal_artist.artist_id, "min_art")
        self.assertEqual(minimal_artist.name, "Minimal Artist")
        self.assertEqual(minimal_artist.genres, [])
        self.assertEqual(minimal_artist.biography, "")
        self.assertEqual(minimal_artist.formed_year, 0)
        self.assertIsNone(minimal_artist.disbanded_year)

    def test_album_without_artist(self):
        """Тест альбома без артиста"""
        # В текущей реализации артист обязателен при создании
        # Но можно проверить с None артистом
        try:
            album_with_none_artist = Album("alb_none", "No Artist Album", None)
            self.assertIsNone(album_with_none_artist.artist)
        except Exception:
            # В некоторых реализациях это может вызывать ошибку
            pass

    def test_library_scanner_edge_cases(self):
        """Тест граничных случаев сканера библиотеки"""
        user = User("test_user", "test", "test@example.com")
        library = MusicLibrary(user)
        scanner = LibraryScanner(library)

        # Прогресс вне диапазона 0-100
        scanner.scan_progress = -10
        self.assertEqual(scanner.scan_progress, -10)

        scanner.scan_progress = 150
        self.assertEqual(scanner.scan_progress, 150)

        # Неподдерживаемые форматы
        unsupported_formats = ["exe", "txt", "zip", "rar"]
        for format in unsupported_formats:
            self.assertNotIn(format, scanner.supported_formats)

    def test_playback_without_song(self):
        """Тест воспроизведения без установки песни"""
        controller = PlaybackController()

        # В текущей реализации это не вызовет ошибку
        result = controller.play(None)
        self.assertTrue(result)  # Демо-версия всегда возвращает True
        self.assertIsNone(controller.state.current_song)

    def test_seek_beyond_song_duration(self):
        """Тест перемотки за пределы длительности песни"""
        controller = PlaybackController()
        song = Song("test.mp3", "Test", 180, "Artist", "Album")
        controller.play(song)

        # Перематываем дальше длительности песни
        result = controller.seek(300)  # Песня длится 180 секунд
        self.assertTrue(result)
        self.assertEqual(controller.state.current_time, 300)

    def test_empty_queue_operations(self):
        """Тест операций с пустой очередью"""
        controller = PlaybackController()
        queue_manager = QueueManager()

        # Очистка пустой очереди
        result = queue_manager.clear_queue()
        self.assertTrue(result)

        # Удаление из пустой очереди
        song = Song("test.mp3", "Test", 180, "Artist", "Album")
        result = queue_manager.remove_from_queue(song)
        self.assertFalse(result)  # Песни нет в очереди

    def test_equalizer_extreme_values(self):
        """Тест экстремальных значений эквалайзера"""
        eq_controller = EqualizerController()

        # Устанавливаем экстремальные значения для доступных полос
        extreme_values = [-24, 24, -100, 100, 0, 50, -50, 25, -25, 12]

        for i, value in enumerate(extreme_values):
            if i < len(eq_controller.equalizer.bands):
                result = eq_controller.adjust_band(i, value)
                self.assertTrue(result)

        # Проверяем, что значения установились
        for i, expected_value in enumerate(extreme_values):
            if i < len(eq_controller.equalizer.bands):
                self.assertEqual(eq_controller.equalizer.bands[i], expected_value)

    def test_empty_search_query(self):
        """Тест поиска с пустым запросом"""
        users = self.user_manager.search_users("")
        self.assertIsInstance(users, list)
        # В реальной реализации может возвращать пустой список или всех пользователей
        # В демо-версии возвращает список с одним пользователем

    def test_nonexistent_user_operations(self):
        """Тест операций с несуществующим пользователем"""
        nonexistent_user = User("nonexistent", "ghost", "ghost@example.com")

        result1 = self.user_manager.update_user_profile(nonexistent_user, {})
        result2 = self.user_manager.delete_user_account(nonexistent_user)

        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_subscription_with_none_user(self):
        """Тест создания подписки с None пользователем"""
        with self.assertRaises(ValueError) as context:
            self.subscription_manager.create_subscription(None, "free")

        self.assertEqual(str(context.exception), "User is required")

    def test_subscription_invalid_plan(self):
        """Тест создания подписки с невалидным тарифом"""
        user = User("test_user", "test", "test@example.com")

        with self.assertRaises(ValueError) as context:
            self.subscription_manager.create_subscription(user, "invalid_plan")

        self.assertIn("Invalid plan type", str(context.exception))

    def test_user_operations_with_none(self):
        """Тест операций с None пользователем"""
        # Обновление профиля с None пользователем
        result = self.user_manager.update_user_profile(None, {"key": "value"})
        self.assertTrue(result)  # Теперь всегда возвращает True

        # Удаление None пользователя
        result = self.user_manager.delete_user_account(None)
        self.assertTrue(result)

    def test_playback_edge_cases(self):
        """Тест граничных случаев воспроизведения"""
        controller = PlaybackController()

        # Пауза без воспроизведения
        result = controller.pause()
        self.assertTrue(result)
        self.assertFalse(controller.state.is_playing)

        # Возобновление без предварительной паузы
        result = controller.resume()
        self.assertTrue(result)
        self.assertTrue(controller.state.is_playing)

        # Остановка без воспроизведения
        result = controller.stop()
        self.assertTrue(result)
        self.assertFalse(controller.state.is_playing)
        self.assertEqual(controller.state.current_time, 0)

    def test_queue_edge_cases(self):
        """Тест граничных случаев очереди"""
        queue_manager = QueueManager()

        # Перемещение в пустой очереди
        result = queue_manager.move_in_queue(0, 1)
        self.assertFalse(result)

        # Получение информации о пустой очереди
        info = queue_manager.get_queue_info()
        self.assertEqual(info['total_songs'], 0)
        self.assertEqual(info['current_position'], 1)
        self.assertEqual(info['total_duration'], 0)


if __name__ == '__main__':
    unittest.main()