import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.AudioModels.Song import Song
from Behaviors.PlaylistBehaviors.PlaylistManager import PlaylistManager
from Behaviors.UserBehaviors.UserManager import UserManager
from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager
from Behaviors.PlayerBehaviors.PlaybackController import PlaybackController
from Exceptions.DuplicateSongException import DuplicateSongException


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()
        self.playlist_manager = PlaylistManager()
        self.subscription_manager = SubscriptionManager()
        self.playback_controller = PlaybackController()

        self.user = self.user_manager.register_user("integration_user", "integration@test.com", "password123")
        self.playlist = self.playlist_manager.create_playlist("Integration Playlist", self.user)

        self.song1 = Song("/music/int1.mp3", "Integration Song 1", 180, "Int Artist 1", "Int Album 1")
        self.song2 = Song("/music/int2.mp3", "Integration Song 2", 200, "Int Artist 2", "Int Album 2")

    def test_user_playlist_integration(self):
        """Тест интеграции пользователя и плейлиста"""
        # Создаем плейлист
        playlist = self.playlist_manager.create_playlist("User Playlist", self.user)

        # Проверяем ассоциации
        self.assertEqual(playlist.creator, self.user)
        self.assertEqual(playlist.name, "User Playlist")

        # Добавляем песни
        playlist.add_song(self.song1)
        playlist.add_song(self.song2)

        # Проверяем содержимое
        self.assertEqual(len(playlist.songs), 2)
        self.assertIn(self.song1, playlist.songs)
        self.assertIn(self.song2, playlist.songs)

    def test_playback_integration(self):
        """Тест интеграции воспроизведения"""
        # Воспроизводим песню
        self.playback_controller.play(self.song1)

        # Проверяем состояние
        self.assertEqual(self.playback_controller.state.current_song, self.song1)
        self.assertTrue(self.playback_controller.state.is_playing)

        # Пауза
        self.playback_controller.pause()
        self.assertFalse(self.playback_controller.state.is_playing)

        # Следующий трек (должен работать даже без очереди)
        result = self.playback_controller.next_track()
        # В данном случае должен вернуть False, так как очередь пуста
        self.assertFalse(result)


    def test_duplicate_song_prevention(self):
        """Тест предотвращения дублирования песен"""
        # Добавляем первую песню
        self.playlist.add_song(self.song1)

        # Пытаемся добавить дубликат
        with self.assertRaises(DuplicateSongException):
            self.playlist.add_song(self.song1)

        # Вторая песня добавляется нормально
        self.playlist.add_song(self.song2)
        self.assertEqual(len(self.playlist.songs), 2)


if __name__ == '__main__':
    unittest.main()