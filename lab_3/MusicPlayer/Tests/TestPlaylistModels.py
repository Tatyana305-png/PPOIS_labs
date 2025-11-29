import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.PlaylistModels.Playlist import Playlist
from Models.PlaylistModels.PlaylistStatistics import PlaylistStatistics
from Models.PlaylistModels.SmartPlaylist import SmartPlaylist
from Models.PlaylistModels.CollaborativePlaylist import CollaborativePlaylist
from Models.AudioModels.Song import Song
from Models.UserModels.User import User
from Exceptions.PlaylistEmptyException import PlaylistEmptyException
from Exceptions.DuplicateSongException import DuplicateSongException


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
        self.playlist.add_song(self.song1)
        self.playlist.add_song(self.song2)
        stats = PlaylistStatistics(self.playlist)
        self.assertEqual(stats.playlist, self.playlist)


class TestCollaborativePlaylist(unittest.TestCase):

    def setUp(self):
        self.creator = User("user123", "creator", "creator@example.com")
        self.collaborator1 = User("user456", "collab1", "collab1@example.com")
        self.collaborator2 = User("user789", "collab2", "collab2@example.com")
        self.non_collaborator = User("user999", "noncollab", "noncollab@example.com")
        self.collab_playlist = CollaborativePlaylist("cpl123", "Collaborative Playlist", self.creator)

    def test_initial_state(self):
        """Тест начального состояния collaborative плейлиста"""
        self.assertEqual(self.collab_playlist.playlist_id, "cpl123")
        self.assertEqual(self.collab_playlist.name, "Collaborative Playlist")
        self.assertEqual(self.collab_playlist.creator, self.creator)
        self.assertEqual(self.collab_playlist.collaborators, [])
        self.assertEqual(self.collab_playlist.edit_permissions, "all")
        self.assertFalse(self.collab_playlist.approval_required)

    def test_add_collaborator(self):
        """Тест добавления collaborator'а"""
        result = self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertTrue(result)
        self.assertEqual(len(self.collab_playlist.collaborators), 1)
        self.assertIn(self.collaborator1, self.collab_playlist.collaborators)

    def test_add_duplicate_collaborator(self):
        """Тест добавления уже существующего collaborator'а"""
        self.collab_playlist.add_collaborator(self.collaborator1)
        result = self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertFalse(result)
        self.assertEqual(len(self.collab_playlist.collaborators), 1)

    def test_add_none_collaborator(self):
        """Тест добавления None в качестве collaborator'а"""
        result = self.collab_playlist.add_collaborator(None)
        self.assertFalse(result)
        self.assertEqual(len(self.collab_playlist.collaborators), 0)

    def test_remove_collaborator(self):
        """Тест удаления collaborator'а"""
        self.collab_playlist.add_collaborator(self.collaborator1)
        result = self.collab_playlist.remove_collaborator(self.collaborator1)
        self.assertTrue(result)
        self.assertEqual(len(self.collab_playlist.collaborators), 0)

    def test_remove_nonexistent_collaborator(self):
        """Тест удаления несуществующего collaborator'а"""
        result = self.collab_playlist.remove_collaborator(self.collaborator1)
        self.assertFalse(result)
        self.assertEqual(len(self.collab_playlist.collaborators), 0)

    def test_get_collaborator_count(self):
        """Тест получения количества collaborator'ов"""
        self.assertEqual(self.collab_playlist.get_collaborator_count(), 0)

        self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertEqual(self.collab_playlist.get_collaborator_count(), 1)

        self.collab_playlist.add_collaborator(self.collaborator2)
        self.assertEqual(self.collab_playlist.get_collaborator_count(), 2)

    def test_is_collaborative(self):
        """Тест проверки, является ли плейлист collaborative"""
        self.assertFalse(self.collab_playlist.is_collaborative())

        self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertTrue(self.collab_playlist.is_collaborative())

    def test_can_user_edit_creator(self):
        """Тест проверки прав редактирования для создателя"""
        self.assertTrue(self.collab_playlist.can_user_edit(self.creator))

    def test_can_user_edit_collaborator_all_permissions(self):
        """Тест проверки прав редактирования для collaborator'а с permissions='all'"""
        self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertTrue(self.collab_playlist.can_user_edit(self.collaborator1))

    def test_can_user_edit_collaborator_approved_permissions_no_approval(self):
        """Тест проверки прав редактирования для collaborator'а с permissions='approved' и без требования approval"""
        self.collab_playlist.edit_permissions = "approved"
        self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertTrue(self.collab_playlist.can_user_edit(self.collaborator1))

    def test_can_user_edit_collaborator_approved_permissions_with_approval(self):
        """Тест проверки прав редактирования для collaborator'а с permissions='approved' и требованием approval"""
        self.collab_playlist.edit_permissions = "approved"
        self.collab_playlist.approval_required = True
        self.collab_playlist.add_collaborator(self.collaborator1)
        self.assertFalse(self.collab_playlist.can_user_edit(self.collaborator1))

    def test_can_user_edit_non_collaborator(self):
        """Тест проверки прав редактирования для пользователя, не являющегося collaborator'ом"""
        self.assertFalse(self.collab_playlist.can_user_edit(self.non_collaborator))

    def test_can_user_edit_after_removal(self):
        """Тест проверки прав редактирования после удаления collaborator'а"""
        self.collab_playlist.add_collaborator(self.collaborator1)
        self.collab_playlist.remove_collaborator(self.collaborator1)
        self.assertFalse(self.collab_playlist.can_user_edit(self.collaborator1))

    def test_multiple_collaborators(self):
        """Тест работы с несколькими collaborator'ами"""
        # Добавляем нескольких collaborator'ов
        self.collab_playlist.add_collaborator(self.collaborator1)
        self.collab_playlist.add_collaborator(self.collaborator2)

        self.assertEqual(self.collab_playlist.get_collaborator_count(), 2)
        self.assertTrue(self.collab_playlist.is_collaborative())

        # Проверяем права для всех collaborator'ов
        self.assertTrue(self.collab_playlist.can_user_edit(self.collaborator1))
        self.assertTrue(self.collab_playlist.can_user_edit(self.collaborator2))

        # Удаляем одного collaborator'а
        self.collab_playlist.remove_collaborator(self.collaborator1)
        self.assertEqual(self.collab_playlist.get_collaborator_count(), 1)
        self.assertFalse(self.collab_playlist.can_user_edit(self.collaborator1))
        self.assertTrue(self.collab_playlist.can_user_edit(self.collaborator2))

    def test_edge_cases_permissions(self):
        """Тест граничных случаев для разрешений"""
        # Пользователь None
        self.assertFalse(self.collab_playlist.can_user_edit(None))

        # Пустой список collaborator'ов с разными настройками permissions
        self.collab_playlist.edit_permissions = "approved"
        self.assertFalse(self.collab_playlist.can_user_edit(self.collaborator1))


if __name__ == '__main__':
    unittest.main()