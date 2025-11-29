import unittest
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.UserModels.User import User
from Models.UserModels.UserStatistics import UserStatistics
from Models.UserModels.UserPreferences import UserPreferences
from Models.UserModels.UserProfile import UserProfile
from Models.UserModels.Subscription import Subscription
from Models.UserModels.ListeningHistory import ListeningHistory
from Exceptions.SubscriptionExpiredException import SubscriptionExpiredException


class TestUserModels(unittest.TestCase):

    def setUp(self):
        self.user = User("user123", "testuser", "test@example.com")
        self.profile = UserProfile(self.user)
        self.subscription = Subscription(self.user)
        self.history = ListeningHistory(self.user)

    def test_user_creation(self):
        self.assertEqual(self.user.user_id, "user123")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)

    def test_user_profile_association(self):
        self.assertEqual(self.profile.user, self.user)
        self.profile.first_name = "John"
        self.profile.last_name = "Doe"
        self.assertEqual(self.profile.first_name, "John")
        self.assertEqual(self.profile.last_name, "Doe")

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan_type, "free")
        self.assertTrue(self.subscription.is_active)

    def test_subscription_validity_valid(self):
        self.subscription.end_date = datetime.now() + timedelta(days=30)
        try:
            self.subscription.check_validity()
            self.assertTrue(True)
        except SubscriptionExpiredException:
            self.fail("Valid subscription raised exception")

    def test_subscription_validity_expired(self):
        self.subscription.end_date = datetime(2020, 1, 1)
        with self.assertRaises(SubscriptionExpiredException):
            self.subscription.check_validity()

    def test_listening_history_association(self):
        self.assertEqual(self.history.user, self.user)
        self.assertEqual(self.history.entries, [])
        self.assertEqual(self.history.total_listening_time, 0)

    def test_user_preferences_defaults(self):
        self.user.preferences = {"theme": "dark", "language": "en"}
        self.assertEqual(self.user.preferences["theme"], "dark")
        self.assertEqual(self.user.preferences["language"], "en")


class TestUserStatistics(unittest.TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User("user123", "testuser", "test@example.com")

        # Создаем статистику пользователя
        self.stats = UserStatistics(self.user)

    def test_user_statistics_initialization(self):
        """Тест инициализации статистики пользователя"""
        self.assertEqual(self.stats.user, self.user)
        self.assertEqual(self.stats.songs_played, 0)
        self.assertEqual(self.stats.artists_discovered, 0)
        self.assertEqual(self.stats.playlists_created, 0)
        self.assertEqual(self.stats.favorites_count, 0)
        self.assertEqual(self.stats.weekly_listening_time, 0)

    def test_increment_songs_played(self):
        """Тест увеличения счетчика прослушанных песен"""
        self.assertEqual(self.stats.songs_played, 0)

        # Увеличиваем несколько раз
        self.stats.increment_songs_played()
        self.assertEqual(self.stats.songs_played, 1)

        self.stats.increment_songs_played()
        self.assertEqual(self.stats.songs_played, 2)

        self.stats.increment_songs_played()
        self.assertEqual(self.stats.songs_played, 3)

    def test_increment_artists_discovered(self):
        """Тест увеличения счетчика обнаруженных артистов"""
        self.assertEqual(self.stats.artists_discovered, 0)

        # Увеличиваем несколько раз
        self.stats.increment_artists_discovered()
        self.assertEqual(self.stats.artists_discovered, 1)

        self.stats.increment_artists_discovered()
        self.assertEqual(self.stats.artists_discovered, 2)

    def test_increment_playlists_created(self):
        """Тест увеличения счетчика созданных плейлистов"""
        self.assertEqual(self.stats.playlists_created, 0)

        # Увеличиваем несколько раз
        self.stats.increment_playlists_created()
        self.assertEqual(self.stats.playlists_created, 1)

        self.stats.increment_playlists_created()
        self.assertEqual(self.stats.playlists_created, 2)

        self.stats.increment_playlists_created()
        self.assertEqual(self.stats.playlists_created, 3)

    def test_update_weekly_listening_positive_minutes(self):
        """Тест обновления недельного времени прослушивания с положительными минутами"""
        self.assertEqual(self.stats.weekly_listening_time, 0)

        # Добавляем время
        self.stats.update_weekly_listening(60)  # 1 час
        self.assertEqual(self.stats.weekly_listening_time, 60)

        self.stats.update_weekly_listening(30)  # 30 минут
        self.assertEqual(self.stats.weekly_listening_time, 90)

        self.stats.update_weekly_listening(120)  # 2 часа
        self.assertEqual(self.stats.weekly_listening_time, 210)

    def test_update_weekly_listening_zero_minutes(self):
        """Тест обновления недельного времени с нулевыми минутами"""
        self.stats.weekly_listening_time = 100

        self.stats.update_weekly_listening(0)

        # Время не должно измениться
        self.assertEqual(self.stats.weekly_listening_time, 100)

    def test_update_weekly_listening_negative_minutes(self):
        """Тест обновления недельного времени с отрицательными минутами"""
        self.stats.weekly_listening_time = 100

        self.stats.update_weekly_listening(-50)

        # Время не должно измениться
        self.assertEqual(self.stats.weekly_listening_time, 100)

    def test_get_statistics_summary_empty(self):
        """Тест получения сводки статистики при нулевых значениях"""
        summary = self.stats.get_statistics_summary()

        expected_summary = {
            'songs_played': 0,
            'artists_discovered': 0,
            'playlists_created': 0,
            'favorites_count': 0,
            'weekly_listening_hours': 0.0
        }

        self.assertEqual(summary, expected_summary)

    def test_get_statistics_summary_with_data(self):
        """Тест получения сводки статистики с данными"""
        # Устанавливаем различные значения
        self.stats.songs_played = 150
        self.stats.artists_discovered = 45
        self.stats.playlists_created = 12
        self.stats.favorites_count = 23
        self.stats.weekly_listening_time = 375  # 6.25 часов

        summary = self.stats.get_statistics_summary()

        expected_summary = {
            'songs_played': 150,
            'artists_discovered': 45,
            'playlists_created': 12,
            'favorites_count': 23,
            'weekly_listening_hours': 6.2  # 375 / 60 = 6.25, округляется до 6.2
        }

        self.assertEqual(summary, expected_summary)

    def test_get_statistics_summary_weekly_listening_rounding(self):
        """Тест округления недельного времени прослушивания"""
        # Проверяем различные значения для округления
        test_cases = [
            (30, 0.5),  # 30 минут = 0.5 часов
            (45, 0.8),  # 45 минут = 0.75 → 0.8
            (90, 1.5),  # 90 минут = 1.5 часов
            (125, 2.1),  # 125 минут = 2.083 → 2.1
            (180, 3.0),  # 180 минут = 3.0 часов
            (277, 4.6),  # 277 минут = 4.616 → 4.6
        ]

        for minutes, expected_hours in test_cases:
            with self.subTest(minutes=minutes, expected_hours=expected_hours):
                self.stats.weekly_listening_time = minutes
                summary = self.stats.get_statistics_summary()
                self.assertEqual(summary['weekly_listening_hours'], expected_hours)

    def test_favorites_count_assignment(self):
        """Тест прямого присвоения счетчика избранного"""
        self.assertEqual(self.stats.favorites_count, 0)

        self.stats.favorites_count = 10
        self.assertEqual(self.stats.favorites_count, 10)

        self.stats.favorites_count = 25
        self.assertEqual(self.stats.favorites_count, 25)

    def test_multiple_increments(self):
        """Тест множественных увеличений разных счетчиков"""
        # Увеличиваем все счетчики по несколько раз
        for _ in range(3):
            self.stats.increment_songs_played()

        for _ in range(2):
            self.stats.increment_artists_discovered()

        for _ in range(4):
            self.stats.increment_playlists_created()

        # Проверяем итоговые значения
        self.assertEqual(self.stats.songs_played, 3)
        self.assertEqual(self.stats.artists_discovered, 2)
        self.assertEqual(self.stats.playlists_created, 4)

    def test_comprehensive_statistics_workflow(self):
        """Тест комплексного рабочего процесса статистики"""
        # Симулируем активность пользователя
        self.stats.increment_songs_played()  # Прослушана 1 песня
        self.stats.increment_artists_discovered()  # Обнаружен 1 артист
        self.stats.update_weekly_listening(45)  # 45 минут прослушивания

        self.stats.increment_songs_played()  # Прослушана 2 песня
        self.stats.increment_playlists_created()  # Создан 1 плейлист
        self.stats.update_weekly_listening(30)  # Еще 30 минут

        self.stats.increment_songs_played()  # Прослушана 3 песня
        self.stats.increment_artists_discovered()  # Обнаружен 2 артист
        self.stats.favorites_count = 5  # 5 избранных треков

        # Проверяем итоговую статистику
        summary = self.stats.get_statistics_summary()

        expected_summary = {
            'songs_played': 3,
            'artists_discovered': 2,
            'playlists_created': 1,
            'favorites_count': 5,
            'weekly_listening_hours': 1.2  # (45 + 30) / 60 = 1.25 → 1.2
        }

        self.assertEqual(summary, expected_summary)

    def test_statistics_independence(self):
        """Тест независимости статистики разных пользователей"""
        user2 = User("user456", "anotheruser", "another@example.com")
        stats2 = UserStatistics(user2)

        # Изменяем статистику первого пользователя
        self.stats.increment_songs_played()
        self.stats.increment_artists_discovered()

        # Статистика второго пользователя не должна измениться
        self.assertEqual(stats2.songs_played, 0)
        self.assertEqual(stats2.artists_discovered, 0)

        # Проверяем что пользователи разные
        self.assertNotEqual(self.stats.user, stats2.user)

    def test_large_numbers_handling(self):
        """Тест обработки больших чисел в статистике"""
        # Устанавливаем большие значения
        self.stats.songs_played = 10000
        self.stats.artists_discovered = 5000
        self.stats.playlists_created = 200
        self.stats.favorites_count = 1500
        self.stats.weekly_listening_time = 10080  # 1 неделя в минутах

        summary = self.stats.get_statistics_summary()

        self.assertEqual(summary['songs_played'], 10000)
        self.assertEqual(summary['artists_discovered'], 5000)
        self.assertEqual(summary['playlists_created'], 200)
        self.assertEqual(summary['favorites_count'], 1500)
        self.assertEqual(summary['weekly_listening_hours'], 168.0)  # 10080 / 60 = 168

    def test_weekly_listening_precision(self):
        """Тест точности вычисления недельного времени"""
        # Проверяем что используется правильное округление (1 decimal)
        self.stats.weekly_listening_time = 61  # 1.0166 часов

        summary = self.stats.get_statistics_summary()
        self.assertEqual(summary['weekly_listening_hours'], 1.0)

        self.stats.weekly_listening_time = 67  # 1.1166 часов
        summary = self.stats.get_statistics_summary()
        self.assertEqual(summary['weekly_listening_hours'], 1.1)

    def test_user_reference_integrity(self):
        """Тест целостности ссылки на пользователя"""
        self.assertEqual(self.stats.user.user_id, "user123")
        self.assertEqual(self.stats.user.username, "testuser")
        self.assertEqual(self.stats.user.email, "test@example.com")

        # Изменяем пользователя (хотя в реальности это маловероятно)
        self.stats.user.username = "updateduser"
        self.assertEqual(self.stats.user.username, "updateduser")

    def test_statistics_after_reset(self):
        """Тест статистики после сброса значений"""
        # Сначала накапливаем статистику
        self.stats.songs_played = 50
        self.stats.artists_discovered = 20
        self.stats.playlists_created = 5
        self.stats.weekly_listening_time = 300

        # "Сбрасываем" статистику (в реальном приложении может быть метод reset)
        self.stats.songs_played = 0
        self.stats.artists_discovered = 0
        self.stats.playlists_created = 0
        self.stats.weekly_listening_time = 0

        summary = self.stats.get_statistics_summary()

        expected_summary = {
            'songs_played': 0,
            'artists_discovered': 0,
            'playlists_created': 0,
            'favorites_count': 0,
            'weekly_listening_hours': 0.0
        }

        self.assertEqual(summary, expected_summary)


    def test_increment_methods_chaining(self):
        """Тест цепочного вызова методов увеличения"""
        # Методы не возвращают значения, но проверяем что они работают последовательно
        self.stats.increment_songs_played()
        self.stats.increment_artists_discovered()
        self.stats.increment_playlists_created()

        self.assertEqual(self.stats.songs_played, 1)
        self.assertEqual(self.stats.artists_discovered, 1)
        self.assertEqual(self.stats.playlists_created, 1)

    def test_statistics_with_different_users(self):
        """Тест статистики с разными пользователями"""
        user1 = User("user1", "user1", "user1@example.com")
        user2 = User("user2", "user2", "user2@example.com")

        stats1 = UserStatistics(user1)
        stats2 = UserStatistics(user2)

        # Добавляем статистику для первого пользователя
        stats1.increment_songs_played()
        stats1.increment_playlists_created()

        # Добавляем статистику для второго пользователя
        stats2.increment_songs_played()
        stats2.increment_songs_played()
        stats2.increment_artists_discovered()

        # Проверяем что статистика независима
        self.assertEqual(stats1.songs_played, 1)
        self.assertEqual(stats1.playlists_created, 1)
        self.assertEqual(stats1.artists_discovered, 0)

        self.assertEqual(stats2.songs_played, 2)
        self.assertEqual(stats2.playlists_created, 0)
        self.assertEqual(stats2.artists_discovered, 1)


class TestUserPreferences(unittest.TestCase):

    def setUp(self):
        self.preferences = UserPreferences()

    def test_user_preferences_initialization(self):
        """Тест инициализации пользовательских предпочтений"""
        self.assertEqual(self.preferences.audio_quality, "high")
        self.assertTrue(self.preferences.auto_play)
        self.assertEqual(self.preferences.crossfade_duration, 0)
        self.assertEqual(self.preferences.equalizer_preset, "flat")
        self.assertFalse(self.preferences.replay_gain)
        self.assertEqual(self.preferences.volume_limit, 100)
        self.assertEqual(self.preferences.keyboard_shortcuts, {})

    def test_set_audio_quality_valid(self):
        """Тест установки валидного качества аудио"""
        valid_qualities = ["low", "medium", "high", "very_high"]

        for quality in valid_qualities:
            with self.subTest(quality=quality):
                result = self.preferences.set_audio_quality(quality)
                self.assertTrue(result)
                self.assertEqual(self.preferences.audio_quality, quality)

    def test_set_audio_quality_invalid(self):
        """Тест установки невалидного качества аудио"""
        invalid_qualities = ["", "invalid", "super_high", "LOW", "HIGH", None, 123]

        for quality in invalid_qualities:
            with self.subTest(quality=quality):
                original_quality = self.preferences.audio_quality

                result = self.preferences.set_audio_quality(quality)

                self.assertFalse(result)
                self.assertEqual(self.preferences.audio_quality, original_quality)

    def test_set_audio_quality_case_sensitive(self):
        """Тест чувствительности к регистру в качестве аудио"""
        mixed_case_qualities = ["Low", "MEDIUM", "High", "Very_High"]

        for quality in mixed_case_qualities:
            with self.subTest(quality=quality):
                original_quality = self.preferences.audio_quality

                result = self.preferences.set_audio_quality(quality)

                self.assertFalse(result)
                self.assertEqual(self.preferences.audio_quality, original_quality)

    def test_set_crossfade_valid_duration(self):
        """Тест установки валидной длительности кроссфейда"""
        valid_durations = [0, 1, 5, 10]

        for duration in valid_durations:
            with self.subTest(duration=duration):
                result = self.preferences.set_crossfade(duration)
                self.assertTrue(result)
                self.assertEqual(self.preferences.crossfade_duration, duration)

    def test_set_crossfade_invalid_duration(self):
        """Тест установки невалидной длительности кроссфейда"""
        invalid_durations = [-1, -5, 11, 15, 100]

        for duration in invalid_durations:
            with self.subTest(duration=duration):
                original_duration = self.preferences.crossfade_duration

                result = self.preferences.set_crossfade(duration)

                self.assertFalse(result)
                self.assertEqual(self.preferences.crossfade_duration, original_duration)

    def test_set_crossfade_boundary_values(self):
        """Тест граничных значений для кроссфейда"""
        # Граничные значения: 0 и 10
        result1 = self.preferences.set_crossfade(0)
        self.assertTrue(result1)
        self.assertEqual(self.preferences.crossfade_duration, 0)

        result2 = self.preferences.set_crossfade(10)
        self.assertTrue(result2)
        self.assertEqual(self.preferences.crossfade_duration, 10)

    def test_set_volume_limit_valid(self):
        """Тест установки валидного лимита громкости"""
        valid_limits = [0, 25, 50, 75, 100]

        for limit in valid_limits:
            with self.subTest(limit=limit):
                result = self.preferences.set_volume_limit(limit)
                self.assertTrue(result)
                self.assertEqual(self.preferences.volume_limit, limit)

    def test_set_volume_limit_invalid(self):
        """Тест установки невалидного лимита громкости"""
        invalid_limits = [-1, -10, 101, 150, -100]

        for limit in invalid_limits:
            with self.subTest(limit=limit):
                original_limit = self.preferences.volume_limit

                result = self.preferences.set_volume_limit(limit)

                self.assertFalse(result)
                self.assertEqual(self.preferences.volume_limit, original_limit)

    def test_set_volume_limit_boundary_values(self):
        """Тест граничных значений для лимита громкости"""
        # Граничные значения: 0 и 100
        result1 = self.preferences.set_volume_limit(0)
        self.assertTrue(result1)
        self.assertEqual(self.preferences.volume_limit, 0)

        result2 = self.preferences.set_volume_limit(100)
        self.assertTrue(result2)
        self.assertEqual(self.preferences.volume_limit, 100)

    def test_add_keyboard_shortcut_valid(self):
        """Тест добавления валидного клавиатурного сокращения"""
        shortcuts = [
            ("play", "Space"),
            ("pause", "Space"),
            ("next_track", "Ctrl+Right"),
            ("previous_track", "Ctrl+Left"),
            ("volume_up", "Ctrl+Up"),
            ("volume_down", "Ctrl+Down")
        ]

        for action, shortcut in shortcuts:
            with self.subTest(action=action, shortcut=shortcut):
                self.preferences.add_keyboard_shortcut(action, shortcut)
                self.assertIn(action, self.preferences.keyboard_shortcuts)
                self.assertEqual(self.preferences.keyboard_shortcuts[action], shortcut)

    def test_add_keyboard_shortcut_empty_action(self):
        """Тест добавления сокращения с пустым действием"""
        initial_shortcuts = self.preferences.keyboard_shortcuts.copy()

        self.preferences.add_keyboard_shortcut("", "Ctrl+P")

        self.assertEqual(self.preferences.keyboard_shortcuts, initial_shortcuts)

    def test_add_keyboard_shortcut_empty_shortcut(self):
        """Тест добавления сокращения с пустым сочетанием"""
        initial_shortcuts = self.preferences.keyboard_shortcuts.copy()

        self.preferences.add_keyboard_shortcut("play", "")

        self.assertEqual(self.preferences.keyboard_shortcuts, initial_shortcuts)

    def test_add_keyboard_shortcut_both_empty(self):
        """Тест добавления сокращения с пустыми действием и сочетанием"""
        initial_shortcuts = self.preferences.keyboard_shortcuts.copy()

        self.preferences.add_keyboard_shortcut("", "")

        self.assertEqual(self.preferences.keyboard_shortcuts, initial_shortcuts)

    def test_add_keyboard_shortcut_overwrite(self):
        """Тест перезаписи существующего сокращения"""
        # Добавляем первоначальное сокращение
        self.preferences.add_keyboard_shortcut("play", "Space")
        self.assertEqual(self.preferences.keyboard_shortcuts["play"], "Space")

        # Перезаписываем
        self.preferences.add_keyboard_shortcut("play", "Ctrl+P")
        self.assertEqual(self.preferences.keyboard_shortcuts["play"], "Ctrl+P")

        # Проверяем что только один ключ
        self.assertEqual(len(self.preferences.keyboard_shortcuts), 1)

    def test_get_playback_settings_default(self):
        """Тест получения настроек воспроизведения по умолчанию"""
        settings = self.preferences.get_playback_settings()

        expected_settings = {
            'audio_quality': 'high',
            'auto_play': True,
            'crossfade_duration': 0,
            'equalizer_preset': 'flat',
            'volume_limit': 100
        }

        self.assertEqual(settings, expected_settings)

    def test_get_playback_settings_custom(self):
        """Тест получения настроек воспроизведения с пользовательскими значениями"""
        # Настраиваем параметры
        self.preferences.set_audio_quality("very_high")
        self.preferences.auto_play = False
        self.preferences.set_crossfade(5)
        self.preferences.equalizer_preset = "rock"
        self.preferences.set_volume_limit(80)

        settings = self.preferences.get_playback_settings()

        expected_settings = {
            'audio_quality': 'very_high',
            'auto_play': False,
            'crossfade_duration': 5,
            'equalizer_preset': 'rock',
            'volume_limit': 80
        }

        self.assertEqual(settings, expected_settings)

    def test_auto_play_assignment(self):
        """Тест присвоения авто-воспроизведения"""
        self.assertTrue(self.preferences.auto_play)

        self.preferences.auto_play = False
        self.assertFalse(self.preferences.auto_play)

        self.preferences.auto_play = True
        self.assertTrue(self.preferences.auto_play)

    def test_equalizer_preset_assignment(self):
        """Тест присвоения пресета эквалайзера"""
        self.assertEqual(self.preferences.equalizer_preset, "flat")

        self.preferences.equalizer_preset = "rock"
        self.assertEqual(self.preferences.equalizer_preset, "rock")

        self.preferences.equalizer_preset = "jazz"
        self.assertEqual(self.preferences.equalizer_preset, "jazz")

        self.preferences.equalizer_preset = "custom"
        self.assertEqual(self.preferences.equalizer_preset, "custom")

    def test_replay_gain_assignment(self):
        """Тест присвоения Replay Gain"""
        self.assertFalse(self.preferences.replay_gain)

        self.preferences.replay_gain = True
        self.assertTrue(self.preferences.replay_gain)

        self.preferences.replay_gain = False
        self.assertFalse(self.preferences.replay_gain)

    def test_multiple_preferences_changes(self):
        """Тест множественных изменений предпочтений"""
        # Проверяем начальные значения
        self.assertEqual(self.preferences.audio_quality, "high")
        self.assertEqual(self.preferences.crossfade_duration, 0)
        self.assertEqual(self.preferences.volume_limit, 100)
        self.assertEqual(self.preferences.keyboard_shortcuts, {})

        # Меняем несколько настроек
        self.preferences.set_audio_quality("medium")
        self.preferences.set_crossfade(3)
        self.preferences.set_volume_limit(75)
        self.preferences.auto_play = False
        self.preferences.equalizer_preset = "pop"
        self.preferences.replay_gain = True
        self.preferences.add_keyboard_shortcut("play", "Space")

        # Проверяем изменения
        self.assertEqual(self.preferences.audio_quality, "medium")
        self.assertEqual(self.preferences.crossfade_duration, 3)
        self.assertEqual(self.preferences.volume_limit, 75)
        self.assertFalse(self.preferences.auto_play)
        self.assertEqual(self.preferences.equalizer_preset, "pop")
        self.assertTrue(self.preferences.replay_gain)
        self.assertEqual(self.preferences.keyboard_shortcuts["play"], "Space")

        # Получаем настройки воспроизведения
        settings = self.preferences.get_playback_settings()
        self.assertEqual(settings['audio_quality'], "medium")
        self.assertEqual(settings['crossfade_duration'], 3)
        self.assertEqual(settings['volume_limit'], 75)
        self.assertEqual(settings['auto_play'], False)
        self.assertEqual(settings['equalizer_preset'], "pop")

    def test_keyboard_shortcuts_multiple_actions(self):
        """Тест множественных клавиатурных сокращений"""
        shortcuts = {
            "play": "Space",
            "pause": "Space",
            "next": "Ctrl+Right",
            "previous": "Ctrl+Left",
            "volume_up": "Ctrl+Up",
            "volume_down": "Ctrl+Down",
            "mute": "Ctrl+M"
        }

        for action, shortcut in shortcuts.items():
            self.preferences.add_keyboard_shortcut(action, shortcut)

        self.assertEqual(len(self.preferences.keyboard_shortcuts), 7)

        for action, expected_shortcut in shortcuts.items():
            self.assertEqual(self.preferences.keyboard_shortcuts[action], expected_shortcut)

    def test_preferences_independence(self):
        """Тест независимости экземпляров предпочтений"""
        preferences1 = UserPreferences()
        preferences2 = UserPreferences()

        # Меняем настройки в первом экземпляре
        preferences1.set_audio_quality("low")
        preferences1.set_crossfade(7)
        preferences1.add_keyboard_shortcut("play", "Space")

        # Второй экземпляр не должен измениться
        self.assertEqual(preferences2.audio_quality, "high")
        self.assertEqual(preferences2.crossfade_duration, 0)
        self.assertEqual(preferences2.keyboard_shortcuts, {})


    def test_audio_quality_edge_cases(self):
        """Тест граничных случаев для качества аудио"""
        # Пустая строка
        result = self.preferences.set_audio_quality("")
        self.assertFalse(result)

        # Строка с пробелами
        result = self.preferences.set_audio_quality(" high ")
        self.assertFalse(result)

        # Числовое значение
        result = self.preferences.set_audio_quality(123)
        self.assertFalse(result)

    def test_get_playback_settings_excludes_some_fields(self):
        """Тест что get_playback_settings не включает все поля"""
        settings = self.preferences.get_playback_settings()

        # Должны быть включены только определенные поля
        expected_keys = {'audio_quality', 'auto_play', 'crossfade_duration',
                         'equalizer_preset', 'volume_limit'}

        self.assertEqual(set(settings.keys()), expected_keys)

        # Эти поля не должны быть в результате
        self.assertNotIn('replay_gain', settings)
        self.assertNotIn('keyboard_shortcuts', settings)

    def test_comprehensive_preferences_workflow(self):
        """Тест комплексного рабочего процесса предпочтений"""
        # Пользователь настраивает все параметры
        self.preferences.set_audio_quality("very_high")
        self.preferences.auto_play = False
        self.preferences.set_crossfade(2)
        self.preferences.equalizer_preset = "rock"
        self.preferences.replay_gain = True
        self.preferences.set_volume_limit(85)

        # Добавляем несколько горячих клавиш
        self.preferences.add_keyboard_shortcut("play_pause", "Space")
        self.preferences.add_keyboard_shortcut("next_track", "Ctrl+Right")
        self.preferences.add_keyboard_shortcut("previous_track", "Ctrl+Left")
        self.preferences.add_keyboard_shortcut("volume_up", "Ctrl+Up")
        self.preferences.add_keyboard_shortcut("volume_down", "Ctrl+Down")

        # Проверяем все настройки
        self.assertEqual(self.preferences.audio_quality, "very_high")
        self.assertFalse(self.preferences.auto_play)
        self.assertEqual(self.preferences.crossfade_duration, 2)
        self.assertEqual(self.preferences.equalizer_preset, "rock")
        self.assertTrue(self.preferences.replay_gain)
        self.assertEqual(self.preferences.volume_limit, 85)
        self.assertEqual(len(self.preferences.keyboard_shortcuts), 5)

        # Проверяем настройки воспроизведения
        playback_settings = self.preferences.get_playback_settings()
        self.assertEqual(playback_settings['audio_quality'], "very_high")
        self.assertEqual(playback_settings['auto_play'], False)
        self.assertEqual(playback_settings['crossfade_duration'], 2)
        self.assertEqual(playback_settings['equalizer_preset'], "rock")
        self.assertEqual(playback_settings['volume_limit'], 85)

if __name__ == '__main__':
    unittest.main()