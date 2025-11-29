import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.PlayerBehaviors.PlaybackController import PlaybackController
from Behaviors.PlayerBehaviors.QueueManager import QueueManager
from Behaviors.PlayerBehaviors.EqualizerController import EqualizerController
from Models.AudioModels.Song import Song

class TestPlayerBehaviorsIntegration(unittest.TestCase):
    """Интеграционные тесты для поведения плеера"""

    def setUp(self):
        self.playback_controller = PlaybackController()
        self.queue_manager = QueueManager()
        self.equalizer_controller = EqualizerController()

        self.song1 = Song("/music/song1.mp3", "Song 1", 180, "Artist 1", "Album 1")
        self.song2 = Song("/music/song2.mp3", "Song 2", 200, "Artist 2", "Album 2")
        self.song3 = Song("/music/song3.mp3", "Song 3", 220, "Artist 3", "Album 3")

        # Используем одну очередь для всех менеджеров
        self.queue_manager.queue = self.playback_controller.queue

    def test_complete_playback_workflow(self):
        """Тест полного workflow воспроизведения"""
        # 1. Добавляем песни в очередь
        self.queue_manager.add_to_queue(self.song1)
        self.queue_manager.add_to_queue(self.song2)
        self.queue_manager.add_to_queue(self.song3)

        # 2. Настраиваем эквалайзер
        self.equalizer_controller.equalizer.is_enabled = True
        self.equalizer_controller.adjust_band(0, 3)  # Усиливаем басы
        self.equalizer_controller.adjust_band(9, 2)  # Усиливаем высокие

        # 3. Воспроизводим
        self.playback_controller.play(self.song1)

        # 4. Переходим к следующему треку
        self.playback_controller.next_track()

        # 5. Настраиваем громкость
        self.playback_controller.set_volume(80)

        # Проверяем состояние
        self.assertEqual(len(self.playback_controller.queue.songs), 3)
        self.assertEqual(self.playback_controller.queue.current_index, 1)
        self.assertEqual(self.playback_controller.state.current_song, self.song2)
        self.assertEqual(self.playback_controller.state.volume, 80)
        self.assertTrue(self.equalizer_controller.equalizer.is_enabled)
        self.assertEqual(self.equalizer_controller.equalizer.bands[0], 3)


    def test_equalizer_preset_workflow(self):
        """Тест workflow работы с пресетами эквалайзера"""
        # 1. Создаем кастомный пресет
        custom_bands = [4, 3, 2, 1, 0, 0, 1, 2, 3, 4]
        self.equalizer_controller.equalizer.bands = custom_bands
        self.equalizer_controller.save_preset("v_shape")

        # 2. Сбрасываем эквалайзер
        self.equalizer_controller.reset_equalizer()
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

        # 3. Применяем сохраненный пресет
        self.equalizer_controller.set_preset("v_shape")
        self.assertEqual(self.equalizer_controller.equalizer.bands, custom_bands)

        # 4. Включаем эквалайзер
        self.equalizer_controller.equalizer.is_enabled = True

        # Проверяем
        self.assertTrue(self.equalizer_controller.equalizer.is_enabled)
        self.assertIn("v_shape", self.equalizer_controller.equalizer.presets)

if __name__ == '__main__':
    unittest.main()