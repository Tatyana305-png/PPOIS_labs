import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Validator import Validator


class TestValidator(unittest.TestCase):


    def test_validate_audio_file(self):
        """Тест валидации аудиофайлов"""
        valid_files = [
            "song.mp3",
            "track.wav",
            "audio.flac",
            "music.aac",
            "/path/to/song.mp3",
            "file.WAV",
            "file.MP3",
            "file.FLAC",
            "file.AAC"
        ]

        invalid_files = [
            "document.pdf",
            "image.jpg",
            "video.mp4",
            "text.txt",
            "script.py",
            "archive.zip",
            "",  # Пустая строка
            "file.",  # Нет расширения
            "file",  # Нет точки
            "file.unknown",
            None,  # None значение
        ]

        for file_path in valid_files:
            with self.subTest(file_path=file_path):
                self.assertTrue(Validator.validate_audio_file(file_path))

        for file_path in invalid_files:
            with self.subTest(file_path=file_path):
                self.assertFalse(Validator.validate_audio_file(file_path))

    def test_validate_playlist_name(self):
        """Тест валидации имени плейлиста"""
        valid_names = [
            "My Playlist",
            "A",  # Минимальная длина
            "x" * 100,  # Максимальная длина
            "Rock & Roll",
            "2024 Hits",
            "  Valid Name  ",  # С пробелами по краям
        ]

        invalid_names = [
            "",  # Пустая строка
            "   ",  # Только пробелы
            "x" * 101,  # Слишком длинное имя
            "\t",  # Только табуляция
            "\n",  # Только новая строка
            None,  # None значение
        ]

        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(Validator.validate_playlist_name(name))

        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(Validator.validate_playlist_name(name))

    def test_validate_edge_cases(self):
        """Тест граничных случаев валидации"""
        # None значения
        self.assertFalse(Validator.validate_email(None))
        self.assertFalse(Validator.validate_audio_file(None))
        self.assertFalse(Validator.validate_playlist_name(None))

        # Числовые значения
        self.assertFalse(Validator.validate_email(123))
        self.assertFalse(Validator.validate_audio_file(123))
        self.assertFalse(Validator.validate_playlist_name(123))

    def test_validate_audio_file_case_insensitive(self):
        """Тест валидации аудиофайлов без учета регистра"""
        mixed_case_files = [
            "song.Mp3",
            "track.Wav",
            "AUDIO.FLAC",
            "Music.AAC",
            "mixed.CaSe.Mp3"
        ]

        for file_path in mixed_case_files:
            with self.subTest(file_path=file_path):
                self.assertTrue(Validator.validate_audio_file(file_path))


if __name__ == '__main__':
    unittest.main()