import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.PlayerModels.PlayerSettings import PlayerSettings


class TestPlayerSettings(unittest.TestCase):

    def setUp(self):
        self.settings = PlayerSettings()

    def test_player_settings_initialization(self):
        """Тест инициализации настроек плеера"""
        self.assertIsNone(self.settings.audio_device)
        self.assertFalse(self.settings.volume_normalization)
        self.assertTrue(self.settings.gapless_playback)
        self.assertEqual(self.settings.crossfade_duration, 0)
        self.assertTrue(self.settings.high_quality_streaming)
        self.assertEqual(self.settings.download_quality, "high")

    def test_enable_volume_normalization(self):
        """Тест включения нормализации громкости"""
        self.assertFalse(self.settings.volume_normalization)

        self.settings.enable_volume_normalization()

        self.assertTrue(self.settings.volume_normalization)

    def test_disable_volume_normalization(self):
        """Тест выключения нормализации громкости"""
        # Включаем сначала
        self.settings.volume_normalization = True
        self.assertTrue(self.settings.volume_normalization)

        self.settings.disable_volume_normalization()

        self.assertFalse(self.settings.volume_normalization)

    def test_set_crossfade_valid_duration(self):
        """Тест установки валидной длительности кроссфейда"""
        valid_durations = [0, 1, 5, 10]

        for duration in valid_durations:
            with self.subTest(duration=duration):
                result = self.settings.set_crossfade(duration)
                self.assertTrue(result)
                self.assertEqual(self.settings.crossfade_duration, duration)

    def test_set_crossfade_invalid_duration(self):
        """Тест установки невалидной длительности кроссфейда"""
        invalid_durations = [-1, -5, 11, 15, 100]

        for duration in invalid_durations:
            with self.subTest(duration=duration):
                # Сохраняем текущее значение
                original_duration = self.settings.crossfade_duration

                result = self.settings.set_crossfade(duration)

                self.assertFalse(result)
                # Значение не должно измениться
                self.assertEqual(self.settings.crossfade_duration, original_duration)

    def test_set_crossfade_boundary_values(self):
        """Тест граничных значений для кроссфейда"""
        # Граничные значения: 0 и 10
        result1 = self.settings.set_crossfade(0)
        self.assertTrue(result1)
        self.assertEqual(self.settings.crossfade_duration, 0)

        result2 = self.settings.set_crossfade(10)
        self.assertTrue(result2)
        self.assertEqual(self.settings.crossfade_duration, 10)

    def test_set_download_quality_valid(self):
        """Тест установки валидного качества загрузки"""
        valid_qualities = ["low", "medium", "high", "very_high"]

        for quality in valid_qualities:
            with self.subTest(quality=quality):
                result = self.settings.set_download_quality(quality)
                self.assertTrue(result)
                self.assertEqual(self.settings.download_quality, quality)

    def test_set_download_quality_invalid(self):
        """Тест установки невалидного качества загрузки"""
        invalid_qualities = ["", "invalid", "super_high", "LOW", "HIGH", None, 123]

        for quality in invalid_qualities:
            with self.subTest(quality=quality):
                # Сохраняем текущее значение
                original_quality = self.settings.download_quality

                result = self.settings.set_download_quality(quality)

                self.assertFalse(result)
                # Значение не должно измениться
                self.assertEqual(self.settings.download_quality, original_quality)

    def test_set_download_quality_case_sensitive(self):
        """Тест чувствительности к регистру в качестве загрузки"""
        # Качество должно быть в нижнем регистре
        mixed_case_qualities = ["Low", "MEDIUM", "High", "Very_High"]

        for quality in mixed_case_qualities:
            with self.subTest(quality=quality):
                original_quality = self.settings.download_quality

                result = self.settings.set_download_quality(quality)

                self.assertFalse(result)
                self.assertEqual(self.settings.download_quality, original_quality)

    def test_get_audio_settings(self):
        """Тест получения аудио-настроек"""
        # Настраиваем некоторые параметры
        self.settings.volume_normalization = True
        self.settings.gapless_playback = False
        self.settings.crossfade_duration = 3
        self.settings.high_quality_streaming = False
        self.settings.download_quality = "medium"

        audio_settings = self.settings.get_audio_settings()

        expected_settings = {
            'volume_normalization': True,
            'gapless_playback': False,
            'crossfade_duration': "3s",
            'high_quality_streaming': False,
            'download_quality': "medium"
        }

        self.assertEqual(audio_settings, expected_settings)

    def test_get_audio_settings_default(self):
        """Тест получения настроек по умолчанию"""
        audio_settings = self.settings.get_audio_settings()

        expected_settings = {
            'volume_normalization': False,
            'gapless_playback': True,
            'crossfade_duration': "0s",
            'high_quality_streaming': True,
            'download_quality': "high"
        }

        self.assertEqual(audio_settings, expected_settings)

    def test_audio_device_assignment(self):
        """Тест присвоения аудио-устройства"""
        self.assertIsNone(self.settings.audio_device)

        # Присваиваем устройство
        self.settings.audio_device = "Speakers"

        self.assertEqual(self.settings.audio_device, "Speakers")

        # Меняем устройство
        self.settings.audio_device = "Headphones"

        self.assertEqual(self.settings.audio_device, "Headphones")

    def test_volume_normalization_toggle(self):
        """Тест переключения нормализации громкости"""
        self.assertFalse(self.settings.volume_normalization)

        # Включаем
        self.settings.enable_volume_normalization()
        self.assertTrue(self.settings.volume_normalization)

        # Выключаем
        self.settings.disable_volume_normalization()
        self.assertFalse(self.settings.volume_normalization)

        # Снова включаем
        self.settings.enable_volume_normalization()
        self.assertTrue(self.settings.volume_normalization)

    def test_gapless_playback_assignment(self):
        """Тест присвоения бесшовного воспроизведения"""
        self.assertTrue(self.settings.gapless_playback)

        # Выключаем
        self.settings.gapless_playback = False
        self.assertFalse(self.settings.gapless_playback)

        # Включаем обратно
        self.settings.gapless_playback = True
        self.assertTrue(self.settings.gapless_playback)

    def test_high_quality_streaming_assignment(self):
        """Тест присвоения высококачественного стриминга"""
        self.assertTrue(self.settings.high_quality_streaming)

        # Выключаем
        self.settings.high_quality_streaming = False
        self.assertFalse(self.settings.high_quality_streaming)

        # Включаем обратно
        self.settings.high_quality_streaming = True
        self.assertTrue(self.settings.high_quality_streaming)

    def test_multiple_settings_changes(self):
        """Тест множественных изменений настроек"""
        # Проверяем начальные значения
        self.assertFalse(self.settings.volume_normalization)
        self.assertEqual(self.settings.crossfade_duration, 0)
        self.assertEqual(self.settings.download_quality, "high")

        # Меняем несколько настроек
        self.settings.enable_volume_normalization()
        self.settings.set_crossfade(5)
        self.settings.set_download_quality("medium")
        self.settings.gapless_playback = False

        # Проверяем изменения
        self.assertTrue(self.settings.volume_normalization)
        self.assertEqual(self.settings.crossfade_duration, 5)
        self.assertEqual(self.settings.download_quality, "medium")
        self.assertFalse(self.settings.gapless_playback)

        # Получаем все настройки
        audio_settings = self.settings.get_audio_settings()
        self.assertEqual(audio_settings['volume_normalization'], True)
        self.assertEqual(audio_settings['crossfade_duration'], "5s")
        self.assertEqual(audio_settings['download_quality'], "medium")
        self.assertEqual(audio_settings['gapless_playback'], False)

    def test_crossfade_duration_string_format(self):
        """Тест формата строки длительности кроссфейда"""
        test_cases = [
            (0, "0s"),
            (1, "1s"),
            (5, "5s"),
            (10, "10s")
        ]

        for duration, expected_string in test_cases:
            with self.subTest(duration=duration, expected=expected_string):
                self.settings.set_crossfade(duration)
                audio_settings = self.settings.get_audio_settings()
                self.assertEqual(audio_settings['crossfade_duration'], expected_string)

    def test_settings_independence(self):
        """Тест независимости экземпляров настроек"""
        settings1 = PlayerSettings()
        settings2 = PlayerSettings()

        # Меняем настройки в первом экземпляре
        settings1.enable_volume_normalization()
        settings1.set_crossfade(3)
        settings1.set_download_quality("low")

        # Второй экземпляр не должен измениться
        self.assertFalse(settings2.volume_normalization)
        self.assertEqual(settings2.crossfade_duration, 0)
        self.assertEqual(settings2.download_quality, "high")

    def test_download_quality_priority_order(self):
        """Тест порядка приоритета качеств загрузки"""
        # Проверяем, что "very_high" является допустимым значением
        result = self.settings.set_download_quality("very_high")
        self.assertTrue(result)
        self.assertEqual(self.settings.download_quality, "very_high")


    def test_download_quality_edge_cases(self):
        """Тест граничных случаев для качества загрузки"""
        # Пустая строка
        result = self.settings.set_download_quality("")
        self.assertFalse(result)

        # Строка с пробелами
        result = self.settings.set_download_quality(" high ")
        self.assertFalse(result)

        # Числовое значение
        result = self.settings.set_download_quality(123)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()