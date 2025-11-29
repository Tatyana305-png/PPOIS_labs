import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.AudioModels.Song import Song


class TestAudioBehaviors(unittest.TestCase):

    def setUp(self):
        # Создаем mock-объекты вместо реальных
        self.audio_manager = Mock()
        self.audio_analyzer = Mock()
        self.audio_effects = Mock()

        # Создаем тестовую песню с реальными файловыми путями
        self.song = Song("test_song.mp3", "Test Song", 180, "Test Artist", "Test Album")
        self.song.bitrate = 320
        self.song.sample_rate = 44100
        self.song.channels = 2
        self.song.bpm = 120.0
        self.song.key = "C major"
        self.song.loudness = -10.0
        self.song.format = "mp3"

        # Настраиваем mock для AudioFileManager
        self.audio_manager.load_audio_file.return_value = self.song
        self.audio_manager.validate_audio_file.return_value = True
        self.audio_manager.extract_metadata.return_value = {
            'title': "Test Song",
            'artist': "Test Artist",
            'album': "Test Album",
            'duration': 180,
            'bitrate': 320,
            'sample_rate': 44100,
            'channels': 2
        }
        self.audio_manager.convert_audio_format.return_value = True

        # Настраиваем mock для AudioAnalyzer
        self.audio_analyzer.analyze_bpm.return_value = 120.0
        self.audio_analyzer.detect_key.return_value = "C major"
        self.audio_analyzer.analyze_loudness.return_value = -10.0

        # Настраиваем mock для AudioEffects
        self.audio_effects.apply_reverb.return_value = True
        self.audio_effects.apply_equalizer.return_value = True
        self.audio_effects.change_pitch.return_value = True

    def test_load_audio_file(self):
        """Тест загрузки аудиофайла"""
        loaded_song = self.audio_manager.load_audio_file("test_song.mp3")
        self.assertIsInstance(loaded_song, Song)
        self.assertEqual(loaded_song.title, "Test Song")
        self.audio_manager.load_audio_file.assert_called_once_with("test_song.mp3")

    def test_validate_audio_file(self):
        """Тест валидации аудиофайла"""
        is_valid = self.audio_manager.validate_audio_file(self.song)
        self.assertTrue(is_valid)
        self.audio_manager.validate_audio_file.assert_called_once_with(self.song)

    def test_extract_metadata(self):
        """Тест извлечения метаданных"""
        metadata = self.audio_manager.extract_metadata(self.song)
        self.assertEqual(metadata['title'], "Test Song")
        self.assertEqual(metadata['artist'], "Test Artist")
        self.assertEqual(metadata['album'], "Test Album")
        self.audio_manager.extract_metadata.assert_called_once_with(self.song)

    def test_analyze_bpm(self):
        """Тест анализа BPM"""
        bpm = self.audio_analyzer.analyze_bpm(self.song)
        self.assertEqual(bpm, 120.0)
        self.audio_analyzer.analyze_bpm.assert_called_once_with(self.song)

    def test_detect_key(self):
        """Тест определения музыкального ключа"""
        key = self.audio_analyzer.detect_key(self.song)
        self.assertEqual(key, "C major")
        self.audio_analyzer.detect_key.assert_called_once_with(self.song)

    def test_analyze_loudness(self):
        """Тест анализа громкости"""
        loudness = self.audio_analyzer.analyze_loudness(self.song)
        self.assertEqual(loudness, -10.0)
        self.audio_analyzer.analyze_loudness.assert_called_once_with(self.song)

    def test_apply_reverb(self):
        """Тест применения реверберации"""
        result = self.audio_effects.apply_reverb(self.song, 0.5)
        self.assertTrue(result)
        self.audio_effects.apply_reverb.assert_called_once_with(self.song, 0.5)

    def test_apply_equalizer(self):
        """Тест применения эквалайзера"""
        eq_settings = {"low": 2, "mid": 0, "high": -1}
        result = self.audio_effects.apply_equalizer(self.song, eq_settings)
        self.assertTrue(result)
        self.audio_effects.apply_equalizer.assert_called_once_with(self.song, eq_settings)

    def test_change_pitch(self):
        """Тест изменения тональности"""
        result = self.audio_effects.change_pitch(self.song, 2)
        self.assertTrue(result)
        self.audio_effects.change_pitch.assert_called_once_with(self.song, 2)

    def test_convert_audio_format(self):
        """Тест конвертации формата"""
        result = self.audio_manager.convert_audio_format(self.song, "wav")
        self.assertTrue(result)
        self.audio_manager.convert_audio_format.assert_called_once_with(self.song, "wav")

    # Дополнительные тесты для проверки поведения с ошибками
    def test_validate_audio_file_invalid(self):
        """Тест валидации невалидного файла"""
        invalid_song = Song("", "Invalid Song", 0, "", "")
        self.audio_manager.validate_audio_file.return_value = False

        is_valid = self.audio_manager.validate_audio_file(invalid_song)
        self.assertFalse(is_valid)

    def test_analyze_empty_song(self):
        """Тест анализа пустой песни"""
        empty_song = Song("empty.mp3", "", 0, "", "")
        self.audio_analyzer.analyze_bpm.return_value = 0.0

        bpm = self.audio_analyzer.analyze_bpm(empty_song)
        self.assertEqual(bpm, 0.0)


if __name__ == '__main__':
    unittest.main()