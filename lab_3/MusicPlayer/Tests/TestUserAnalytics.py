import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.UserAnalytics import UserAnalytics
from Models.UserModels.User import User


class TestUserAnalytics(unittest.TestCase):

    def setUp(self):
        self.analytics = UserAnalytics()

        # Создаем тестового пользователя с историей прослушивания
        self.user = User("user123", "testuser", "test@example.com")

        # Создаем mock объект истории прослушивания
        class ListeningHistoryEntry:
            def __init__(self, duration, artist=None, genre=None):
                self.duration = duration
                self.artist = artist
                self.genre = genre

        class ListeningHistory:
            def __init__(self):
                self.entries = []

        self.user.listening_history = ListeningHistory()

        # Добавляем тестовые записи в историю
        self.user.listening_history.entries = [
            ListeningHistoryEntry(180, "Artist 1", "Rock"),
            ListeningHistoryEntry(200, "Artist 2", "Pop"),
            ListeningHistoryEntry(220, "Artist 1", "Rock"),  # Повторный артист
            ListeningHistoryEntry(240, "Artist 3", "Jazz"),
            ListeningHistoryEntry(260, "Artist 4", "Pop"),
            ListeningHistoryEntry(280, "Artist 5", "Electronic"),
            ListeningHistoryEntry(300, "Artist 6", "Rock"),  # Еще рок
            ListeningHistoryEntry(320, "Artist 7", "Hip-Hop"),
        ]

    def test_user_analytics_initialization(self):
        """Тест инициализации аналитики"""
        self.assertIsInstance(self.analytics, UserAnalytics)

    def test_get_listening_stats_with_user(self):
        """Тест получения статистики прослушивания с пользователем"""
        stats = self.analytics.get_listening_stats(self.user)

        self.assertEqual(stats['period'], 'all')
        self.assertEqual(stats['songs_played'], 8)
        self.assertEqual(stats['artists_listened'], 7)  # 7 уникальных артистов
        self.assertEqual(stats['total_time'], 180 + 200 + 220 + 240 + 260 + 280 + 300 + 320)

    def test_get_listening_stats_with_period(self):
        """Тест получения статистики с указанием периода"""
        stats = self.analytics.get_listening_stats(self.user, "week")

        self.assertEqual(stats['period'], 'week')
        # Метод _filter_by_period заглушка, поэтому возвращает всю историю
        self.assertEqual(stats['songs_played'], 8)

    def test_get_listening_stats_without_user(self):
        """Тест получения статистики без пользователя"""
        with self.assertRaises(ValueError) as context:
            self.analytics.get_listening_stats(None)

        self.assertEqual(str(context.exception), "User is required")

    def test_get_listening_stats_user_without_history(self):
        """Тест получения статистики для пользователя без истории прослушивания"""
        user_without_history = User("user456", "nohistory", "no@example.com")

        stats = self.analytics.get_listening_stats(user_without_history)

        self.assertEqual(stats['total_time'], 0)
        self.assertEqual(stats['songs_played'], 0)
        self.assertEqual(stats['artists_listened'], 0)
        self.assertEqual(stats['period'], 'all')

    def test_get_favorite_genres(self):
        """Тест получения любимых жанров"""
        favorite_genres = self.analytics.get_favorite_genres(self.user)

        # Rock должен быть первым (3 трека), затем Pop (2 трека)
        expected_genres = ["Rock", "Pop", "Jazz", "Electronic", "Hip-Hop"]
        self.assertEqual(favorite_genres, expected_genres)

    def test_get_favorite_genres_empty_history(self):
        """Тест получения любимых жанров при пустой истории"""
        user_empty = User("empty", "empty", "empty@example.com")
        user_empty.listening_history = type('MockHistory', (), {'entries': []})()

        favorite_genres = self.analytics.get_favorite_genres(user_empty)

        self.assertEqual(favorite_genres, [])

    def test_get_favorite_genres_user_without_history(self):
        """Тест получения любимых жанров для пользователя без истории"""
        user_no_history = User("nohistory", "nohistory", "no@example.com")

        favorite_genres = self.analytics.get_favorite_genres(user_no_history)

        self.assertEqual(favorite_genres, [])

    def test_get_favorite_genres_without_user(self):
        """Тест получения любимых жанров без пользователя"""
        favorite_genres = self.analytics.get_favorite_genres(None)

        self.assertEqual(favorite_genres, [])

    def test_get_favorite_genres_limited_to_top_5(self):
        """Тест что возвращается только топ-5 жанров"""
        # Создаем пользователя с большим количеством жанров
        user_many_genres = User("many", "many", "many@example.com")

        class ListeningHistory:
            def __init__(self):
                self.entries = []

        user_many_genres.listening_history = ListeningHistory()

        # Добавляем много жанров
        genres = ["Rock", "Pop", "Jazz", "Electronic", "Hip-Hop", "Classical", "Blues"]
        for i, genre in enumerate(genres):
            entry = type('MockEntry', (), {'genre': genre})()
            user_many_genres.listening_history.entries.append(entry)

        favorite_genres = self.analytics.get_favorite_genres(user_many_genres)

        # Должны вернуться только первые 5 жанров (в алфавитном порядке, так как все с count=1)
        self.assertEqual(len(favorite_genres), 5)

    def test_generate_listening_report(self):
        """Тест генерации отчета о прослушивании"""
        report = self.analytics.generate_listening_report(self.user)

        self.assertIn("Listening Report for testuser", report)
        self.assertIn("Total listening time:", report)
        self.assertIn("Songs played: 8", report)
        self.assertIn("Artists discovered: 7", report)
        self.assertIn("Favorite genres: Rock, Pop, Jazz, Electronic, Hip-Hop", report)

    def test_generate_listening_report_without_user(self):
        """Тест генерации отчета без пользователя"""
        report = self.analytics.generate_listening_report(None)

        self.assertEqual(report, "No user data")

    def test_generate_listening_report_user_without_history(self):
        """Тест генерации отчета для пользователя без истории"""
        user_no_history = User("nohistory", "nohistory", "no@example.com")

        report = self.analytics.generate_listening_report(user_no_history)

        self.assertIn("Listening Report for nohistory", report)
        self.assertIn("Total listening time: 0 seconds", report)
        self.assertIn("Songs played: 0", report)
        self.assertIn("Artists discovered: 0", report)
        self.assertIn("No genre data available", report)

    def test_generate_listening_report_user_without_genres(self):
        """Тест генерации отчета для пользователя без данных о жанрах"""
        user_no_genres = User("nogenres", "nogenres", "no@example.com")

        class ListeningHistoryEntry:
            def __init__(self, duration, artist):
                self.duration = duration
                self.artist = artist
                # Нет атрибута genre

        class ListeningHistory:
            def __init__(self):
                self.entries = [
                    ListeningHistoryEntry(180, "Artist 1"),
                    ListeningHistoryEntry(200, "Artist 2")
                ]

        user_no_genres.listening_history = ListeningHistory()

        report = self.analytics.generate_listening_report(user_no_genres)

        self.assertIn("Listening Report for nogenres", report)
        self.assertIn("No genre data available", report)

    def test_empty_stats(self):
        """Тест метода получения пустой статистики"""
        empty_stats = self.analytics._get_empty_stats()

        self.assertEqual(empty_stats['total_time'], 0)
        self.assertEqual(empty_stats['songs_played'], 0)
        self.assertEqual(empty_stats['artists_listened'], 0)
        self.assertEqual(empty_stats['period'], 'all')

    def test_filter_by_period(self):
        """Тест фильтрации по периоду (заглушка)"""
        test_history = [1, 2, 3, 4, 5]

        filtered_history = self.analytics._filter_by_period(test_history, "week")

        # Метод заглушка, должен вернуть ту же историю
        self.assertEqual(filtered_history, test_history)

    def test_listening_stats_with_entries_without_duration(self):
        """Тест статистики с записями без длительности"""
        user_partial_data = User("partial", "partial", "partial@example.com")

        class ListeningHistoryEntry:
            def __init__(self, has_duration=True, has_artist=True):
                if has_duration:
                    self.duration = 180
                if has_artist:
                    self.artist = "Test Artist"

        class ListeningHistory:
            def __init__(self):
                self.entries = [
                    ListeningHistoryEntry(has_duration=True, has_artist=True),
                    ListeningHistoryEntry(has_duration=False, has_artist=True),  # Без длительности
                    ListeningHistoryEntry(has_duration=True, has_artist=False),  # Без артиста
                ]

        user_partial_data.listening_history = ListeningHistory()

        stats = self.analytics.get_listening_stats(user_partial_data)

        # Должны учитываться только записи с длительностью
        self.assertEqual(stats['total_time'], 180 * 2)  # Две записи с длительностью
        self.assertEqual(stats['songs_played'], 3)  # Все три записи
        self.assertEqual(stats['artists_listened'], 1)  # Только один уникальный артист

    def test_favorite_genres_case_sensitivity(self):
        """Тест чувствительности к регистру в жанрах"""
        user_mixed_case = User("mixed", "mixed", "mixed@example.com")

        class ListeningHistory:
            def __init__(self):
                self.entries = []

        user_mixed_case.listening_history = ListeningHistory()

        # Добавляем жанры в разном регистре
        genres = ["rock", "Rock", "ROCK", "pop", "Pop"]
        for genre in genres:
            entry = type('MockEntry', (), {'genre': genre})()
            user_mixed_case.listening_history.entries.append(entry)

        favorite_genres = self.analytics.get_favorite_genres(user_mixed_case)

        # Жанры с разным регистром считаются разными
        self.assertEqual(len(favorite_genres), 5)


if __name__ == '__main__':
    unittest.main()