import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Exceptions.AudioException import AudioException
from Exceptions.InvalidAudioFormatException import InvalidAudioFormatException
from Exceptions.AudioCorruptedException import AudioCorruptedException
from Exceptions.AudioPermissionException import AudioPermissionException
from Exceptions.AudioFileNotFoundException import AudioFileNotFoundException
from Exceptions.PlaylistException import PlaylistException
from Exceptions.PlaylistNotFoundException import PlaylistNotFoundException
from Exceptions.PlaylistEmptyException import PlaylistEmptyException
from Exceptions.DuplicateSongException import DuplicateSongException
from Exceptions.UserException import UserException
from Exceptions.UserNotFoundException import UserNotFoundException
from Exceptions.InsufficientPermissionsException import InsufficientPermissionsException
from Exceptions.SubscriptionExpiredException import SubscriptionExpiredException


class TestExceptions(unittest.TestCase):

    def test_audio_exceptions_hierarchy(self):
        self.assertTrue(issubclass(InvalidAudioFormatException, AudioException))
        self.assertTrue(issubclass(AudioCorruptedException, AudioException))
        self.assertTrue(issubclass(AudioPermissionException, AudioException))
        self.assertTrue(issubclass(AudioFileNotFoundException, AudioException))

    def test_playlist_exceptions_hierarchy(self):
        self.assertTrue(issubclass(PlaylistNotFoundException, PlaylistException))
        self.assertTrue(issubclass(PlaylistEmptyException, PlaylistException))
        self.assertTrue(issubclass(DuplicateSongException, PlaylistException))

    def test_user_exceptions_hierarchy(self):
        self.assertTrue(issubclass(UserNotFoundException, UserException))
        self.assertTrue(issubclass(InsufficientPermissionsException, UserException))
        self.assertTrue(issubclass(SubscriptionExpiredException, UserException))

    def test_exception_messages(self):
        # Audio Exceptions
        with self.assertRaises(InvalidAudioFormatException) as context:
            raise InvalidAudioFormatException("Invalid format: xyz")
        self.assertEqual(str(context.exception), "Invalid format: xyz")

        with self.assertRaises(AudioFileNotFoundException) as context:
            raise AudioFileNotFoundException("File not found: song.mp3")
        self.assertEqual(str(context.exception), "File not found: song.mp3")

        # Playlist Exceptions
        with self.assertRaises(PlaylistEmptyException) as context:
            raise PlaylistEmptyException("Playlist is empty")
        self.assertEqual(str(context.exception), "Playlist is empty")

        # User Exceptions
        with self.assertRaises(UserNotFoundException) as context:
            raise UserNotFoundException("User not found")
        self.assertEqual(str(context.exception), "User not found")

    def test_exception_inheritance(self):
        # Проверяем, что исключения правильно наследуются от базовых
        audio_exc = InvalidAudioFormatException()
        self.assertIsInstance(audio_exc, AudioException)

        file_not_found_exc = AudioFileNotFoundException()
        self.assertIsInstance(file_not_found_exc, AudioException)
        self.assertIsInstance(file_not_found_exc, AudioFileNotFoundException)

        playlist_exc = PlaylistEmptyException()
        self.assertIsInstance(playlist_exc, PlaylistException)

        user_exc = UserNotFoundException()
        self.assertIsInstance(user_exc, UserException)

    def test_audio_file_not_found_exception_creation(self):
        """Тест создания AudioFileNotFoundException с различными параметрами"""
        # С сообщением об ошибке
        exception = AudioFileNotFoundException("Audio file 'song.mp3' not found")
        self.assertEqual(str(exception), "Audio file 'song.mp3' not found")

        # Без сообщения (по умолчанию)
        exception_default = AudioFileNotFoundException()
        self.assertEqual(str(exception_default), "")

        # С пустым сообщением
        exception_empty = AudioFileNotFoundException("")
        self.assertEqual(str(exception_empty), "")

    def test_audio_file_not_found_exception_hierarchy_strict(self):
        """Строгая проверка иерархии наследования для AudioFileNotFoundException"""
        exception = AudioFileNotFoundException()

        # Должен быть экземпляром AudioFileNotFoundException
        self.assertIsInstance(exception, AudioFileNotFoundException)

        # Должен быть экземпляром AudioException
        self.assertIsInstance(exception, AudioException)

        # Должен быть экземпляром базового Exception
        self.assertIsInstance(exception, Exception)

        # Не должен быть экземпляром других конкретных исключений
        self.assertNotIsInstance(exception, InvalidAudioFormatException)
        self.assertNotIsInstance(exception, PlaylistException)
        self.assertNotIsInstance(exception, UserException)

    def test_audio_file_not_found_exception_behavior(self):
        """Тест поведения AudioFileNotFoundException при выбросе"""

        def function_that_raises():
            raise AudioFileNotFoundException("File path: /music/nonexistent.mp3")

        # Проверяем, что исключение действительно выбрасывается
        with self.assertRaises(AudioFileNotFoundException) as context:
            function_that_raises()

        # Проверяем сообщение об ошибке
        self.assertEqual(str(context.exception), "File path: /music/nonexistent.mp3")

        # Проверяем тип исключения через isinstance
        self.assertIsInstance(context.exception, AudioFileNotFoundException)
        self.assertIsInstance(context.exception, AudioException)

    def test_all_audio_exceptions_together(self):
        """Тест всех аудио исключений вместе"""
        audio_exceptions = [
            InvalidAudioFormatException("Invalid format"),
            AudioCorruptedException("File corrupted"),
            AudioPermissionException("Permission denied"),
            AudioFileNotFoundException("File not found")
        ]

        for exc in audio_exceptions:
            with self.subTest(exception_type=type(exc).__name__):
                self.assertIsInstance(exc, AudioException)
                self.assertIsInstance(exc, Exception)

    def test_audio_file_not_found_exception_with_file_path(self):
        """Тест AudioFileNotFoundException с конкретными путями к файлам"""
        test_cases = [
            "/music/song.mp3",
            "C:\\Users\\Music\\track.wav",
            "relative/path/audio.flac",
            ""
        ]

        for file_path in test_cases:
            with self.subTest(file_path=file_path):
                if file_path:
                    message = f"Audio file not found: {file_path}"
                    exception = AudioFileNotFoundException(message)
                    self.assertEqual(str(exception), message)
                else:
                    exception = AudioFileNotFoundException()
                    self.assertEqual(str(exception), "")

    def test_exception_chaining(self):
        """Тест цепочки исключений для AudioFileNotFoundException"""
        try:
            try:
                # Имитируем оригинальную ошибку файловой системы
                raise OSError("No such file or directory")
            except OSError as original_error:
                # Оборачиваем в наше кастомное исключение
                raise AudioFileNotFoundException("Audio file missing") from original_error
        except AudioFileNotFoundException as wrapped_error:
            self.assertIsInstance(wrapped_error, AudioFileNotFoundException)
            self.assertIsInstance(wrapped_error.__cause__, OSError)
            self.assertEqual(str(wrapped_error.__cause__), "No such file or directory")


if __name__ == '__main__':
    unittest.main()