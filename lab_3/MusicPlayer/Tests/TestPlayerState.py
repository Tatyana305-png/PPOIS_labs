import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.PlayerModels.PlayerState import PlayerState
from Models.AudioModels.Song import Song


class TestPlayerState(unittest.TestCase):

    def setUp(self):
        self.player_state = PlayerState()
        self.song = Song("/music/test.mp3", "Test Song", 180, "Test Artist", "Test Album")

    def test_player_state_initialization(self):
        """Тест инициализации состояния плеера"""
        self.assertIsNone(self.player_state.current_song)
        self.assertFalse(self.player_state.is_playing)
        self.assertEqual(self.player_state.current_time, 0)
        self.assertEqual(self.player_state.volume, 50)
        self.assertEqual(self.player_state.repeat_mode, "none")
        self.assertFalse(self.player_state.shuffle)
        self.assertEqual(self.player_state.playback_speed, 1.0)

    def test_player_state_with_song(self):
        """Тест состояния плеера с установленной песней"""
        self.player_state.current_song = self.song
        self.player_state.is_playing = True
        self.player_state.current_time = 30.5
        self.player_state.volume = 75
        self.player_state.repeat_mode = "all"
        self.player_state.shuffle = True
        self.player_state.playback_speed = 1.5

        self.assertEqual(self.player_state.current_song, self.song)
        self.assertTrue(self.player_state.is_playing)
        self.assertEqual(self.player_state.current_time, 30.5)
        self.assertEqual(self.player_state.volume, 75)
        self.assertEqual(self.player_state.repeat_mode, "all")
        self.assertTrue(self.player_state.shuffle)
        self.assertEqual(self.player_state.playback_speed, 1.5)

    def test_player_state_volume_limits(self):
        """Тест граничных значений громкости"""
        # Нижняя граница
        self.player_state.volume = 0
        self.assertEqual(self.player_state.volume, 0)

        # Верхняя граница
        self.player_state.volume = 100
        self.assertEqual(self.player_state.volume, 100)

        # Значение по умолчанию
        new_state = PlayerState()
        self.assertEqual(new_state.volume, 50)

    def test_player_state_repeat_modes(self):
        """Тест различных режимов повтора"""
        repeat_modes = ["none", "one", "all"]

        for mode in repeat_modes:
            self.player_state.repeat_mode = mode
            self.assertEqual(self.player_state.repeat_mode, mode)

    def test_player_state_playback_speed(self):
        """Тест скорости воспроизведения"""
        speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

        for speed in speeds:
            self.player_state.playback_speed = speed
            self.assertEqual(self.player_state.playback_speed, speed)


if __name__ == '__main__':
    unittest.main()