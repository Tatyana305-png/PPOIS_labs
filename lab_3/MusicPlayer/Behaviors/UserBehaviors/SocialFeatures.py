from Models.UserModels.User import User
from Models.PlaylistModels.Playlist import Playlist
from Models.AudioModels.Song import Song
from datetime import datetime
from typing import List

class SocialFeatures:
    """Управление социальным шерингом контента"""

    def share_playlist(self, user: User, playlist: Playlist, platform: str) -> bool:
        """Делится плейлистом в социальной сети"""
        if not user or not playlist:
            return False

        valid_platforms = ["twitter", "facebook", "whatsapp", "telegram"]
        if platform not in valid_platforms:
            return False

        print(f"Sharing playlist '{playlist.name}' to {platform}")
        return True

    def send_song_recommendation(self, user: User, friend: User, song: Song) -> bool:
        """Отправляет рекомендацию песни другу"""
        if not user or not friend or not song:
            return False

        if user.user_id == friend.user_id:
            return False

        print(f"Recommending '{song.title}' to {friend.username}")
        return True

    def get_shareable_link(self, playlist: Playlist) -> str:
        """Генерирует shareable ссылку для плейлиста"""
        if not playlist:
            return ""
        return f"musicapp.com/playlist/{playlist.playlist_id}"

    def create_listening_party(self, user: User, playlist: Playlist) -> str:
        """Создает listening party"""
        if not user or not playlist:
            return ""
        party_id = f"party_{int(datetime.now().timestamp())}"
        print(f"Created listening party {party_id} for playlist '{playlist.name}'")
        return party_id

    def join_listening_party(self, user: User, party_id: str) -> bool:
        """Присоединяется к listening party"""
        if not user or not party_id:
            return False
        print(f"User {user.username} joined listening party {party_id}")
        return True

    def view_friend_activity(self, user: User) -> List[dict]:
        """Просматривает активность друзей"""
        if not user:
            return []
        return [
            {"friend": "user1", "activity": "listening to Song 1"},
            {"friend": "user2", "activity": "created a playlist"}
        ]