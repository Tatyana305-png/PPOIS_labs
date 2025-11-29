import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.SocialFeatures import SocialFeatures
from Models.UserModels.User import User
from Models.PlaylistModels.Playlist import Playlist
from Models.AudioModels.Song import Song

class TestSocialFeatures(unittest.TestCase):

    def setUp(self):
        self.social_features = SocialFeatures()
        self.user = User("user1", "testuser", "test@example.com")
        self.friend = User("user2", "friend", "friend@example.com")

        self.playlist = Playlist("pl1", "Test Playlist", self.user)
        self.song = Song("/music/test.mp3", "Test Song", 180, "Test Artist", "Test Album")
        self.playlist.add_song(self.song)

    def test_share_playlist(self):
        """Тест плейлиста"""
        platforms = ["facebook", "twitter", "whatsapp"]

        for platform in platforms:
            result = self.social_features.share_playlist(self.user, self.playlist, platform)
            self.assertTrue(result)

    def test_create_listening_party(self):
        """Тест создания listening party"""
        party_id = self.social_features.create_listening_party(self.user, self.playlist)

        self.assertIsInstance(party_id, str)
        self.assertIn("party", party_id)

    def test_join_listening_party(self):
        """Тест присоединения к listening party"""
        party_id = "test_party_123"
        result = self.social_features.join_listening_party(self.user, party_id)

        self.assertTrue(result)

    def test_send_song_recommendation(self):
        """Тест отправки рекомендации песни"""
        result = self.social_features.send_song_recommendation(self.user, self.friend, self.song)

        self.assertTrue(result)

    def test_view_friend_activity(self):
        """Тест просмотра активности друзей"""
        activity = self.social_features.view_friend_activity(self.user)

        self.assertIsInstance(activity, list)

if __name__ == '__main__':
    unittest.main()