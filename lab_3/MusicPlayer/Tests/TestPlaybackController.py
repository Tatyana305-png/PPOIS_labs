import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.PlayerBehaviors.PlaybackController import PlaybackController
from Models.PlayerModels.PlayerState import PlayerState
from Models.PlayerModels.PlaybackQueue import PlaybackQueue
from Models.AudioModels.Song import Song


class TestPlaybackController(unittest.TestCase):

    def setUp(self):
        self.playback_controller = PlaybackController()
        self.song1 = Song("/music/song1.mp3", "Song 1", 180, "Artist 1", "Album 1")
        self.song2 = Song("/music/song2.mp3", "Song 2", 200, "Artist 2", "Album 2")
        self.song3 = Song("/music/song3.mp3", "Song 3", 220, "Artist 3", "Album 3")

        # Заполняем очередь для тестов
        self.playback_controller.queue.songs = [self.song1, self.song2, self.song3]

    def test_playback_controller_initialization(self):
        """Тест инициализации контроллера воспроизведения"""
        self.assertIsInstance(self.playback_controller.state, PlayerState)
        self.assertIsInstance(self.playback_controller.queue, PlaybackQueue)
        self.assertFalse(self.playback_controller.state.is_playing)
        self.assertIsNone(self.playback_controller.state.current_song)

    def test_play_song(self):
        """Тест воспроизведения песни"""
        result = self.playback_controller.play(self.song1)

        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.current_song, self.song1)
        self.assertTrue(self.playback_controller.state.is_playing)
        self.assertEqual(self.playback_controller.state.current_time, 0)

    def test_pause_playback(self):
        """Тест паузы воспроизведения"""
        # Сначала воспроизводим
        self.playback_controller.play(self.song1)
        self.assertTrue(self.playback_controller.state.is_playing)

        # Ставим на паузу
        result = self.playback_controller.pause()
        self.assertTrue(result)
        self.assertFalse(self.playback_controller.state.is_playing)
        self.assertEqual(self.playback_controller.state.current_song, self.song1)

    def test_resume_playback(self):
        """Тест возобновления воспроизведения"""
        # Воспроизводим и ставим на паузу
        self.playback_controller.play(self.song1)
        self.playback_controller.pause()
        self.assertFalse(self.playback_controller.state.is_playing)

        # Возобновляем
        result = self.playback_controller.resume()
        self.assertTrue(result)
        self.assertTrue(self.playback_controller.state.is_playing)

    def test_stop_playback(self):
        """Тест остановки воспроизведения"""
        # Воспроизводим
        self.playback_controller.play(self.song1)
        self.playback_controller.state.current_time = 30.5

        # Останавливаем
        result = self.playback_controller.stop()
        self.assertTrue(result)
        self.assertFalse(self.playback_controller.state.is_playing)
        self.assertEqual(self.playback_controller.state.current_time, 0)

    def test_next_track_with_queue(self):
        """Тест перехода к следующему треку с заполненной очередью"""
        # Устанавливаем текущую позицию
        self.playback_controller.queue.current_index = 0
        self.playback_controller.state.current_song = self.song1

        # Переходим к следующему треку
        result = self.playback_controller.next_track()
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.queue.current_index, 1)
        self.assertEqual(self.playback_controller.state.current_song, self.song2)

    def test_next_track_at_end_of_queue(self):
        """Тест перехода к следующему треку в конце очереди"""
        # Устанавливаем последнюю позицию
        self.playback_controller.queue.current_index = 2
        self.playback_controller.state.current_song = self.song3

        # Переходим к следующему треку (должен вернуться к началу)
        result = self.playback_controller.next_track()
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.queue.current_index, 0)
        self.assertEqual(self.playback_controller.state.current_song, self.song1)

    def test_next_track_empty_queue(self):
        """Тест перехода к следующему треку с пустой очередью"""
        empty_controller = PlaybackController()
        empty_controller.queue.songs = []

        result = empty_controller.next_track()
        self.assertFalse(result)
        self.assertEqual(empty_controller.queue.current_index, 0)

    def test_previous_track_with_queue(self):
        """Тест перехода к предыдущему треку с заполненной очередью"""
        # Устанавливаем текущую позицию
        self.playback_controller.queue.current_index = 1
        self.playback_controller.state.current_song = self.song2

        # Переходим к предыдущему треку
        result = self.playback_controller.previous_track()
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.queue.current_index, 0)
        self.assertEqual(self.playback_controller.state.current_song, self.song1)

    def test_previous_track_at_start_of_queue(self):
        """Тест перехода к предыдущему треку в начале очереди"""
        # Устанавливаем первую позицию
        self.playback_controller.queue.current_index = 0
        self.playback_controller.state.current_song = self.song1

        # Переходим к предыдущему треку (должен перейти к концу)
        result = self.playback_controller.previous_track()
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.queue.current_index, 2)
        self.assertEqual(self.playback_controller.state.current_song, self.song3)

    def test_seek_forward(self):
        """Тест перемотки вперед"""
        self.playback_controller.play(self.song1)

        result = self.playback_controller.seek(45.7)
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.current_time, 45.7)

    def test_seek_backward(self):
        """Тест перемотки назад"""
        self.playback_controller.play(self.song1)
        self.playback_controller.state.current_time = 60.0

        result = self.playback_controller.seek(30.0)
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.current_time, 30.0)

    def test_seek_negative_time(self):
        """Тест перемотки на отрицательное время"""
        self.playback_controller.play(self.song1)

        result = self.playback_controller.seek(-10.0)
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.current_time, -10.0)

    def test_set_volume_normal_range(self):
        """Тест установки громкости в нормальном диапазоне"""
        volumes = [0, 25, 50, 75, 100]

        for volume in volumes:
            result = self.playback_controller.set_volume(volume)
            self.assertTrue(result)
            self.assertEqual(self.playback_controller.state.volume, volume)

    def test_set_volume_out_of_range(self):
        """Тест установки громкости вне диапазона"""
        # Ниже минимального
        result = self.playback_controller.set_volume(-10)
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.volume, 0)

        # Выше максимального
        result = self.playback_controller.set_volume(150)
        self.assertTrue(result)
        self.assertEqual(self.playback_controller.state.volume, 100)

    def test_set_repeat_mode(self):
        """Тест установки режима повтора"""
        repeat_modes = ["none", "one", "all"]

        for mode in repeat_modes:
            result = self.playback_controller.set_repeat_mode(mode)
            self.assertTrue(result)
            self.assertEqual(self.playback_controller.state.repeat_mode, mode)

    def test_toggle_shuffle(self):
        """Тест переключения перемешивания"""
        # Включаем
        result = self.playback_controller.toggle_shuffle()
        self.assertTrue(result)
        self.assertTrue(self.playback_controller.state.shuffle)

        # Выключаем
        result = self.playback_controller.toggle_shuffle()
        self.assertTrue(result)
        self.assertFalse(self.playback_controller.state.shuffle)

if __name__ == '__main__':
    unittest.main()