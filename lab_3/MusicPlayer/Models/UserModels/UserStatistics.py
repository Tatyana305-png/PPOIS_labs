from typing import Dict
from .User import User

class UserStatistics:
    def __init__(self, user: User):
        self.user = user
        self.songs_played = 0
        self.artists_discovered = 0
        self.playlists_created = 0
        self.favorites_count = 0
        self.weekly_listening_time = 0

    def increment_songs_played(self) -> None:
        """Увеличивает счетчик прослушанных песен"""
        self.songs_played += 1

    def increment_artists_discovered(self) -> None:
        """Увеличивает счетчик обнаруженных артистов"""
        self.artists_discovered += 1

    def increment_playlists_created(self) -> None:
        """Увеличивает счетчик созданных плейлистов"""
        self.playlists_created += 1

    def update_weekly_listening(self, minutes: int) -> None:
        """Обновляет недельное время прослушивания"""
        if minutes > 0:
            self.weekly_listening_time += minutes

    def get_statistics_summary(self) -> Dict:
        """Возвращает сводку статистики пользователя"""
        return {
            'songs_played': self.songs_played,
            'artists_discovered': self.artists_discovered,
            'playlists_created': self.playlists_created,
            'favorites_count': self.favorites_count,
            'weekly_listening_hours': round(self.weekly_listening_time / 60, 1)
        }