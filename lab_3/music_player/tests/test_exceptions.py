import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exceptions.audio_exceptions import (
    AudioException,
    InvalidAudioFormatException,
    AudioFileNotFoundException,
    AudioCorruptedException,
    AudioPermissionException
)
from exceptions.playlist_exceptions import (
    PlaylistException,
    PlaylistNotFoundException,
    PlaylistEmptyException,
    DuplicateSongException
)
from exceptions.user_exceptions import (
    UserException,
    UserNotFoundException,
    InsufficientPermissionsException,
    SubscriptionExpiredException
)


class TestExceptions(unittest.TestCase):

    def test_audio_exceptions_hierarchy(self):
        self.assertTrue(issubclass(InvalidAudioFormatException, AudioException))
        self.assertTrue(issubclass(AudioFileNotFoundException, AudioException))
        self.assertTrue(issubclass(AudioCorruptedException, AudioException))
        self.assertTrue(issubclass(AudioPermissionException, AudioException))

    def test_playlist_exceptions_hierarchy(self):
        self.assertTrue(issubclass(PlaylistNotFoundException, PlaylistException))
        self.assertTrue(issubclass(PlaylistEmptyException, PlaylistException))
        self.assertTrue(issubclass(DuplicateSongException, PlaylistException))

    def test_user_exceptions_hierarchy(self):
        self.assertTrue(issubclass(UserNotFoundException, UserException))
        self.assertTrue(issubclass(InsufficientPermissionsException, UserException))
        self.assertTrue(issubclass(SubscriptionExpiredException, UserException))

    def test_exception_messages(self):
        # Audio exceptions
        with self.assertRaises(InvalidAudioFormatException) as context:
            raise InvalidAudioFormatException("Invalid format: xyz")
        self.assertEqual(str(context.exception), "Invalid format: xyz")

        # Playlist exceptions
        with self.assertRaises(PlaylistEmptyException) as context:
            raise PlaylistEmptyException("Playlist is empty")
        self.assertEqual(str(context.exception), "Playlist is empty")

        # User exceptions
        with self.assertRaises(UserNotFoundException) as context:
            raise UserNotFoundException("User not found")
        self.assertEqual(str(context.exception), "User not found")

    def test_exception_inheritance(self):
        # Проверяем, что исключения правильно наследуются от базовых
        audio_exc = InvalidAudioFormatException()
        self.assertIsInstance(audio_exc, AudioException)

        playlist_exc = PlaylistEmptyException()
        self.assertIsInstance(playlist_exc, PlaylistException)

        user_exc = UserNotFoundException()
        self.assertIsInstance(user_exc, UserException)


if __name__ == '__main__':
    unittest.main()