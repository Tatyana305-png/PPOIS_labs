import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.playlist_models import Playlist, SmartPlaylist, CollaborativePlaylist
from models.audio_models import Song
from models.user_models import User
from exceptions.playlist_exceptions import PlaylistEmptyException, DuplicateSongException


class TestPlaylistModels(unittest.TestCase):

    def setUp(self):
        self.user = User("user123", "testuser", "test@example.com")
        self.playlist = Playlist("pl123", "Test Playlist", self.user)
        self.song1 = Song("/music/song1.mp3", "Song 1", 180, "Artist 1", "Album 1")
        self.song2 = Song("/music/song2.mp3", "Song 2", 200, "Artist 2", "Album 2")

    def test_playlist_creation(self):
        self.assertEqual(self.playlist.playlist_id, "pl123")
        self.assertEqual(self.playlist.name, "Test Playlist")
        self.assertEqual(self.playlist.creator, self.user)
        self.assertEqual(self.playlist.songs, [])

    def test_add_song(self):
        self.playlist.add_song(self.song1)
        self.assertEqual(len(self.playlist.songs), 1)
        self.assertEqual(self.playlist.songs[0], self.song1)

    def test_add_duplicate_song(self):
        self.playlist.add_song(self.song1)
        with self.assertRaises(DuplicateSongException):
            self.playlist.add_song(self.song1)

    def test_remove_song(self):
        self.playlist.add_song(self.song1)
        self.playlist.add_song(self.song2)
        self.playlist.remove_song(self.song1)
        self.assertEqual(len(self.playlist.songs), 1)
        self.assertEqual(self.playlist.songs[0], self.song2)

    def test_remove_from_empty_playlist(self):
        with self.assertRaises(PlaylistEmptyException):
            self.playlist.remove_song(self.song1)

    def test_smart_playlist_creation(self):
        criteria = {"genre": "rock", "max_songs": 50}
        smart_pl = SmartPlaylist("spl123", "Smart Rock", self.user, criteria)
        self.assertEqual(smart_pl.criteria, criteria)
        self.assertTrue(smart_pl.auto_update)

    def test_collaborative_playlist(self):
        collab_pl = CollaborativePlaylist("cpl123", "Collaborative", self.user)
        collaborator = User("user456", "collabuser", "collab@example.com")
        collab_pl.collaborators.append(collaborator)
        self.assertEqual(len(collab_pl.collaborators), 1)
        self.assertEqual(collab_pl.collaborators[0], collaborator)

    def test_playlist_statistics(self):
        from models.playlist_models import PlaylistStatistics
        self.playlist.add_song(self.song1)
        self.playlist.add_song(self.song2)
        stats = PlaylistStatistics(self.playlist)
        self.assertEqual(stats.playlist, self.playlist)


if __name__ == '__main__':
    unittest.main()