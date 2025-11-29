import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.PlaylistBehaviors.PlaylistManager import PlaylistManager
from Behaviors.PlaylistBehaviors.SmartPlaylistGenerator import SmartPlaylistGenerator
from Behaviors.PlaylistBehaviors.PlaylistAnalyzer import PlaylistAnalyzer
from Models.PlaylistModels.Playlist import Playlist
from Models.UserModels.User import User
from Models.AudioModels.Song import Song
from Models.LibraryModels.MusicLibrary import MusicLibrary


class TestPlaylistBehaviors(unittest.TestCase):

    def setUp(self):
        self.playlist_manager = PlaylistManager()
        self.smart_generator = SmartPlaylistGenerator()
        self.playlist_analyzer = PlaylistAnalyzer()
        self.user = User("user123", "testuser", "test@example.com")
        self.library = MusicLibrary(self.user)

        self.playlist = Playlist("pl123", "Test Playlist", self.user)
        self.song1 = Song("/music/song1.mp3", "Rock Song", 180, "Rock Artist", "Rock Album")
        self.song1.genre = "rock"
        self.song1.bpm = 120
        self.song2 = Song("/music/song2.mp3", "Jazz Song", 200, "Jazz Artist", "Jazz Album")
        self.song2.genre = "jazz"
        self.song2.bpm = 90

        self.playlist.add_song(self.song1)
        self.playlist.add_song(self.song2)

    def test_create_playlist(self):
        new_playlist = self.playlist_manager.create_playlist("New Playlist", self.user)
        self.assertIsInstance(new_playlist, Playlist)
        self.assertEqual(new_playlist.name, "New Playlist")
        self.assertEqual(new_playlist.creator, self.user)

    def test_rename_playlist(self):
        result = self.playlist_manager.rename_playlist(self.playlist, "Renamed Playlist")
        self.assertTrue(result)
        self.assertEqual(self.playlist.name, "Renamed Playlist")

    def test_duplicate_playlist(self):
        duplicate = self.playlist_manager.duplicate_playlist(self.playlist)
        self.assertIsInstance(duplicate, Playlist)
        self.assertNotEqual(duplicate.playlist_id, self.playlist.playlist_id)
        self.assertEqual(len(duplicate.songs), len(self.playlist.songs))

    def test_generate_smart_playlist_by_genre(self):
        smart_pl = self.smart_generator.generate_by_genre("rock", self.library, 50)
        self.assertEqual(smart_pl.criteria['genre'], "rock")
        self.assertEqual(smart_pl.criteria['max_songs'], 50)

    def test_calculate_total_duration(self):
        total_duration = self.playlist_analyzer.calculate_total_duration(self.playlist)
        expected_duration = self.song1.duration + self.song2.duration
        self.assertEqual(total_duration, expected_duration)

    def test_get_genre_distribution(self):
        distribution = self.playlist_analyzer.get_genre_distribution(self.playlist)
        self.assertEqual(distribution['rock'], 1)
        self.assertEqual(distribution['jazz'], 1)

    def test_find_duplicates(self):
        # Добавляем дубликат
        self.playlist.songs.append(self.song1)
        duplicates = self.playlist_analyzer.find_duplicates(self.playlist)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], self.song1)

    def test_analyze_playlist_energy(self):
        energy = self.playlist_analyzer.analyze_playlist_energy(self.playlist)
        expected_energy = (self.song1.bpm + self.song2.bpm) / 2
        self.assertEqual(energy, expected_energy)

    def test_get_most_common_artist(self):
        most_common = self.playlist_analyzer.get_most_common_artist(self.playlist)
        # Оба артиста встречаются по одному разу, должен вернуть первого
        self.assertIn(most_common, ["Rock Artist", "Jazz Artist"])


if __name__ == '__main__':
    unittest.main()