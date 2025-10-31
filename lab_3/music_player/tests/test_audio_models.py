import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.audio_models import Song, Podcast, Audiobook
from exceptions.audio_exceptions import InvalidAudioFormatException


class TestAudioModels(unittest.TestCase):

    def setUp(self):
        self.song = Song("/music/test.mp3", "Test Song", 180, "Test Artist", "Test Album")
        self.podcast = Podcast("/podcasts/test.mp3", "Test Podcast", 3600, "Test Host", 1)
        self.audiobook = Audiobook("/books/test.mp3", "Test Book", 7200, "Test Author", "Test Narrator")

    def test_song_creation(self):
        self.assertEqual(self.song.title, "Test Song")
        self.assertEqual(self.song.artist, "Test Artist")
        self.assertEqual(self.song.album, "Test Album")
        self.assertEqual(self.song.duration, 180)

    def test_podcast_creation(self):
        self.assertEqual(self.podcast.title, "Test Podcast")
        self.assertEqual(self.podcast.host, "Test Host")
        self.assertEqual(self.podcast.episode, 1)

    def test_audiobook_creation(self):
        self.assertEqual(self.audiobook.title, "Test Book")
        self.assertEqual(self.audiobook.author, "Test Author")
        self.assertEqual(self.audiobook.narrator, "Test Narrator")

    def test_song_validate_format_valid(self):
        self.song.format = "mp3"
        try:
            self.song.validate_format()
            self.assertTrue(True)
        except InvalidAudioFormatException:
            self.fail("Valid format raised exception")

    def test_song_validate_format_invalid(self):
        self.song.format = "invalid"
        with self.assertRaises(InvalidAudioFormatException):
            self.song.validate_format()

    def test_song_default_values(self):
        self.assertEqual(self.song.bitrate, 320)
        self.assertEqual(self.song.sample_rate, 44100)
        self.assertEqual(self.song.channels, 2)

    def test_podcast_default_values(self):
        self.assertEqual(self.podcast.topic, "")
        self.assertEqual(self.podcast.description, "")

    def test_audiobook_default_values(self):
        self.assertEqual(self.audiobook.chapter, 1)
        self.assertEqual(self.audiobook.total_chapters, 10)


if __name__ == '__main__':
    unittest.main()