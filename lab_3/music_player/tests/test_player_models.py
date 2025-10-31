import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.player_models import PlayerState, Equalizer, AudioDevice, PlaybackQueue, PlayerSettings
from models.audio_models import Song


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


class TestEqualizer(unittest.TestCase):

    def setUp(self):
        self.equalizer = Equalizer()

    def test_equalizer_initialization(self):
        """Тест инициализации эквалайзера"""
        self.assertEqual(len(self.equalizer.bands), 10)
        self.assertEqual(self.equalizer.bands, [0] * 10)
        self.assertEqual(self.equalizer.presets, {})
        self.assertFalse(self.equalizer.is_enabled)
        self.assertEqual(self.equalizer.preamp, 0)

    def test_equalizer_bands_manipulation(self):
        """Тест работы с полосами эквалайзера"""
        # Установка значений для полос
        test_values = [-12, -6, 0, 3, 6, 9, 6, 3, 0, -3]

        for i, value in enumerate(test_values):
            self.equalizer.bands[i] = value

        self.assertEqual(self.equalizer.bands, test_values)

        # Проверка отдельных полос
        self.assertEqual(self.equalizer.bands[0], -12)
        self.assertEqual(self.equalizer.bands[4], 6)
        self.assertEqual(self.equalizer.bands[9], -3)

    def test_equalizer_presets(self):
        """Тест работы с пресетами эквалайзера"""
        # Создание пресетов
        rock_preset = [6, 4, 2, 0, -2, -2, 0, 2, 4, 6]
        jazz_preset = [0, 2, 4, 3, 1, 0, -1, -2, -3, -4]
        classical_preset = [-3, -1, 0, 1, 2, 3, 2, 1, 0, -1]

        self.equalizer.presets = {
            "rock": rock_preset,
            "jazz": jazz_preset,
            "classical": classical_preset
        }

        # Проверка пресетов
        self.assertEqual(len(self.equalizer.presets), 3)
        self.assertEqual(self.equalizer.presets["rock"], rock_preset)
        self.assertEqual(self.equalizer.presets["jazz"], jazz_preset)
        self.assertEqual(self.equalizer.presets["classical"], classical_preset)

    def test_equalizer_enable_disable(self):
        """Тест включения/выключения эквалайзера"""
        self.assertFalse(self.equalizer.is_enabled)

        self.equalizer.is_enabled = True
        self.assertTrue(self.equalizer.is_enabled)

        self.equalizer.is_enabled = False
        self.assertFalse(self.equalizer.is_enabled)

    def test_equalizer_preamp(self):
        """Тест работы с предусилителем"""
        preamp_values = [-12, -6, 0, 3, 6, 12]

        for value in preamp_values:
            self.equalizer.preamp = value
            self.assertEqual(self.equalizer.preamp, value)


class TestAudioDevice(unittest.TestCase):

    def setUp(self):
        self.audio_device = AudioDevice("dev123", "Test Speakers")

    def test_audio_device_initialization(self):
        """Тест инициализации аудиоустройства"""
        self.assertEqual(self.audio_device.device_id, "dev123")
        self.assertEqual(self.audio_device.name, "Test Speakers")
        self.assertEqual(self.audio_device.type, "output")
        self.assertEqual(self.audio_device.sample_rate, 44100)
        self.assertEqual(self.audio_device.buffer_size, 1024)
        self.assertEqual(self.audio_device.latency, 0)
        self.assertFalse(self.audio_device.is_default)

    def test_audio_device_properties(self):
        """Тест свойств аудиоустройства"""
        # Изменение свойств
        self.audio_device.type = "input"
        self.audio_device.sample_rate = 48000
        self.audio_device.buffer_size = 2048
        self.audio_device.latency = 50
        self.audio_device.is_default = True

        self.assertEqual(self.audio_device.type, "input")
        self.assertEqual(self.audio_device.sample_rate, 48000)
        self.assertEqual(self.audio_device.buffer_size, 2048)
        self.assertEqual(self.audio_device.latency, 50)
        self.assertTrue(self.audio_device.is_default)

    def test_audio_device_types(self):
        """Тест различных типов аудиоустройств"""
        device_types = ["output", "input", "virtual", "bluetooth"]

        for device_type in device_types:
            self.audio_device.type = device_type
            self.assertEqual(self.audio_device.type, device_type)

    def test_audio_device_sample_rates(self):
        """Тест различных частот дискретизации"""
        sample_rates = [22050, 44100, 48000, 96000, 192000]

        for rate in sample_rates:
            self.audio_device.sample_rate = rate
            self.assertEqual(self.audio_device.sample_rate, rate)

    def test_audio_device_comparison(self):
        """Тест сравнения аудиоустройств"""
        device1 = AudioDevice("dev1", "Speakers")
        device2 = AudioDevice("dev2", "Headphones")
        device3 = AudioDevice("dev1", "Different Name")  # Тот же ID

        self.assertNotEqual(device1.device_id, device2.device_id)
        self.assertEqual(device1.device_id, device3.device_id)
        self.assertNotEqual(device1.name, device3.name)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для моделей плеера"""

    def test_player_state_edge_cases(self):
        """Тест граничных случаев состояния плеера"""
        player_state = PlayerState()

        # Отрицательное время
        player_state.current_time = -10
        self.assertEqual(player_state.current_time, -10)

        # Слишком большая громкость
        player_state.volume = 150
        self.assertEqual(player_state.volume, 150)

        # Неверный режим повтора (должен работать в демо)
        player_state.repeat_mode = "invalid_mode"
        self.assertEqual(player_state.repeat_mode, "invalid_mode")

    def test_empty_playback_queue(self):
        """Тест пустой очереди воспроизведения"""
        queue = PlaybackQueue()

        self.assertEqual(len(queue.songs), 0)
        self.assertEqual(queue.current_index, 0)
        self.assertEqual(len(queue.history), 0)
        self.assertEqual(len(queue.up_next), 0)

        # Попытка получить текущую песню (должна быть None)
        # В реальной реализации здесь была бы проверка
        if queue.songs:
            current_song = queue.songs[queue.current_index]
        else:
            current_song = None

        self.assertIsNone(current_song)

    def test_equalizer_edge_cases(self):
        """Тест граничных случаев эквалайзера"""
        equalizer = Equalizer()

        # Экстремальные значения для полос
        extreme_values = [-24, -12, 0, 12, 24]
        for i in range(min(5, len(equalizer.bands))):
            equalizer.bands[i] = extreme_values[i]

        # Проверяем, что значения установились
        for i in range(min(5, len(equalizer.bands))):
            self.assertEqual(equalizer.bands[i], extreme_values[i])


if __name__ == '__main__':
    unittest.main()