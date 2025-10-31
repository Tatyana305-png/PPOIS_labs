import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from behaviors.player_behaviors import PlaybackController, QueueManager, EqualizerController, AudioDeviceManager
from models.player_models import PlayerState, Equalizer, PlaybackQueue, AudioDevice
from models.audio_models import Song


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
        # Текущая песня остается установленной (реализация зависит от требований)

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


class TestQueueManager(unittest.TestCase):

    def setUp(self):
        self.queue_manager = QueueManager()
        self.song1 = Song("/music/song1.mp3", "Song 1", 180, "Artist 1", "Album 1")
        self.song2 = Song("/music/song2.mp3", "Song 2", 200, "Artist 2", "Album 2")
        self.song3 = Song("/music/song3.mp3", "Song 3", 220, "Artist 3", "Album 3")

        # Инициализируем очередь
        self.queue_manager.queue = PlaybackQueue()

    def test_add_to_queue(self):
        """Тест добавления песни в очередь"""
        result = self.queue_manager.add_to_queue(self.song1)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 1)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)

        # Добавляем еще одну
        result = self.queue_manager.add_to_queue(self.song2)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song2)

    def test_remove_from_queue_existing_song(self):
        """Тест удаления существующей песни из очереди"""
        # Добавляем песни
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        # Удаляем среднюю
        result = self.queue_manager.remove_from_queue(self.song2)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song3)

    def test_remove_from_queue_nonexistent_song(self):
        """Тест удаления несуществующей песни из очереди"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.remove_from_queue(self.song3)
        self.assertFalse(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)

    def test_clear_queue(self):
        """Тест очистки очереди"""
        # Заполняем очередь
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]
        self.queue_manager.queue.current_index = 1
        self.queue_manager.queue.history = [self.song1]

        # Очищаем
        result = self.queue_manager.clear_queue()
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 0)
        # Текущий индекс и история могут сбрасываться или оставаться (зависит от реализации)

    def test_move_in_queue_valid_positions(self):
        """Тест перемещения песни в очереди с валидными позициями"""
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        # Перемещаем песню с позиции 0 на позицию 2
        result = self.queue_manager.move_in_queue(0, 2)
        self.assertTrue(result)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song2)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song3)
        self.assertEqual(self.queue_manager.queue.songs[2], self.song1)

    def test_move_in_queue_invalid_old_index(self):
        """Тест перемещения с невалидным старым индексом"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.move_in_queue(5, 1)  # Невалидный старый индекс
        self.assertFalse(result)
        # Очередь не должна измениться
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)

    def test_move_in_queue_invalid_new_index(self):
        """Тест перемещения с невалидным новым индексом"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.move_in_queue(0, 5)  # Невалидный новый индекс
        self.assertFalse(result)

    def test_save_queue_as_playlist(self):
        """Тест сохранения очереди как плейлиста"""
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        result = self.queue_manager.save_queue_as_playlist("Test Playlist")
        self.assertTrue(result)


class TestEqualizerController(unittest.TestCase):

    def setUp(self):
        self.equalizer_controller = EqualizerController()

    def test_equalizer_controller_initialization(self):
        """Тест инициализации контроллера эквалайзера"""
        self.assertIsInstance(self.equalizer_controller.equalizer, Equalizer)
        self.assertEqual(len(self.equalizer_controller.equalizer.bands), 10)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_set_preset_existing(self):
        """Тест установки существующего пресета"""
        # Создаем пресеты
        self.equalizer_controller.equalizer.presets = {
            "rock": [6, 4, 2, 0, -2, -2, 0, 2, 4, 6],
            "jazz": [0, 2, 4, 3, 1, 0, -1, -2, -3, -4]
        }

        result = self.equalizer_controller.set_preset("rock")
        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [6, 4, 2, 0, -2, -2, 0, 2, 4, 6])

    def test_set_preset_nonexistent(self):
        """Тест установки несуществующего пресета"""
        self.equalizer_controller.equalizer.presets = {
            "rock": [6, 4, 2, 0, -2, -2, 0, 2, 4, 6]
        }

        result = self.equalizer_controller.set_preset("nonexistent")
        self.assertFalse(result)
        # Полосы не должны измениться
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_adjust_band_valid(self):
        """Тест корректировки валидной полосы"""
        # Корректируем несколько полос
        bands_to_adjust = [(0, -6), (5, 3), (9, 12)]

        for band, value in bands_to_adjust:
            result = self.equalizer_controller.adjust_band(band, value)
            self.assertTrue(result)
            self.assertEqual(self.equalizer_controller.equalizer.bands[band], value)

    def test_adjust_band_invalid_band(self):
        """Тест корректировки невалидной полосы"""
        # Полоса вне диапазона
        result = self.equalizer_controller.adjust_band(-1, 5)
        self.assertFalse(result)

        result = self.equalizer_controller.adjust_band(10, 5)
        self.assertFalse(result)

        # Полосы не должны измениться
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_reset_equalizer(self):
        """Тест сброса эквалайзера"""
        # Устанавливаем ненулевые значения
        for i in range(10):
            self.equalizer_controller.equalizer.bands[i] = i * 2 - 5

        # Сбрасываем
        result = self.equalizer_controller.reset_equalizer()
        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_save_preset(self):
        """Тест сохранения пресета"""
        # Устанавливаем значения полос
        test_bands = [-3, -1, 0, 2, 4, 4, 2, 0, -1, -3]
        self.equalizer_controller.equalizer.bands = test_bands

        # Сохраняем как пресет
        result = self.equalizer_controller.save_preset("custom")
        self.assertTrue(result)
        self.assertIn("custom", self.equalizer_controller.equalizer.presets)
        self.assertEqual(self.equalizer_controller.equalizer.presets["custom"], test_bands)

    def test_save_preset_overwrite(self):
        """Тест перезаписи существующего пресета"""
        # Сохраняем первый пресет
        bands1 = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
        self.equalizer_controller.equalizer.bands = bands1
        self.equalizer_controller.save_preset("test_preset")

        # Сохраняем с тем же именем (перезапись)
        bands2 = [5, 4, 3, 2, 1, 1, 2, 3, 4, 5]
        self.equalizer_controller.equalizer.bands = bands2
        result = self.equalizer_controller.save_preset("test_preset")

        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.presets["test_preset"], bands2)


class TestAudioDeviceManager(unittest.TestCase):

    def setUp(self):
        self.audio_device_manager = AudioDeviceManager()

    def test_audio_device_manager_initialization(self):
        """Тест инициализации менеджера аудиоустройств"""
        self.assertIsNotNone(self.audio_device_manager)

    def test_get_available_devices(self):
        """Тест получения доступных устройств"""
        devices = self.audio_device_manager.get_available_devices()

        self.assertIsInstance(devices, list)
        # В демо-версии может возвращать пустой список

    def test_set_output_device(self):
        """Тест установки выходного устройства"""
        device = AudioDevice("test_dev", "Test Speakers")

        result = self.audio_device_manager.set_output_device(device)
        self.assertTrue(result)

    def test_configure_device_settings(self):
        """Тест конфигурации настроек устройства"""
        device = AudioDevice("test_dev", "Test Device")
        settings = {
            "sample_rate": 48000,
            "buffer_size": 2048,
            "latency": 50
        }

        result = self.audio_device_manager.configure_device_settings(device, settings)
        self.assertTrue(result)

    def test_test_audio_device(self):
        """Тест тестирования аудиоустройства"""
        device = AudioDevice("test_dev", "Test Device")

        result = self.audio_device_manager.test_audio_device(device)
        self.assertTrue(result)


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


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для поведения плеера"""

    def test_playback_without_song(self):
        """Тест воспроизведения без установки песни"""
        controller = PlaybackController()

        # В текущей реализации это не вызовет ошибку
        # В реальной системе здесь была бы проверка
        result = controller.play(None)
        self.assertTrue(result)  # Демо-версия всегда возвращает True

    def test_seek_beyond_song_duration(self):
        """Тест перемотки за пределы длительности песни"""
        controller = PlaybackController()
        song = Song("/music/test.mp3", "Test", 180, "Artist", "Album")
        controller.play(song)

        # Перематываем дальше длительности песни
        result = controller.seek(300)  # Песня длится 180 секунд
        self.assertTrue(result)
        self.assertEqual(controller.state.current_time, 300)

    def test_empty_queue_operations(self):
        """Тест операций с пустой очередью"""
        controller = PlaybackController()
        queue_manager = QueueManager()
        queue_manager.queue = controller.queue

        # Очистка пустой очереди
        result = queue_manager.clear_queue()
        self.assertTrue(result)

        # Удаление из пустой очереди
        song = Song("/music/test.mp3", "Test", 180, "Artist", "Album")
        result = queue_manager.remove_from_queue(song)
        self.assertFalse(result)

    def test_equalizer_extreme_values(self):
        """Тест экстремальных значений эквалайзера"""
        eq_controller = EqualizerController()

        # Устанавливаем экстремальные значения
        extreme_values = [-24, 24, -100, 100, 0, 50, -50, 25, -25, 12]

        for i, value in enumerate(extreme_values):
            if i < len(eq_controller.equalizer.bands):
                eq_controller.adjust_band(i, value)

        # Проверяем, что значения установились
        for i, expected_value in enumerate(extreme_values):
            if i < len(eq_controller.equalizer.bands):
                self.assertEqual(eq_controller.equalizer.bands[i], expected_value)


if __name__ == '__main__':
    unittest.main()