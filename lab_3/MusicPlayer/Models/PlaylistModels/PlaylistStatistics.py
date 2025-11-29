from .Playlist import Playlist
from typing import Dict

class PlaylistStatistics:
    def __init__(self, playlist: Playlist):
        self.playlist = playlist
        self.total_duration = 0
        self.avg_rating = 0
        self.genre_distribution = {}
        self.most_played_song = None

    def calculate_total_duration(self) -> float:
        """Вычисляет общую длительность плейлиста"""
        self.total_duration = sum(song.duration for song in self.playlist.songs)
        return self.total_duration

    def analyze_genre_distribution(self) -> Dict:
        """Анализирует распределение жанров в плейлисте"""
        distribution = {}
        for song in self.playlist.songs:
            if hasattr(song, 'genre'):
                genre = song.genre
                distribution[genre] = distribution.get(genre, 0) + 1

        self.genre_distribution = distribution
        return distribution

    def get_most_common_genre(self) -> str:
        """Возвращает самый частый жанр в плейлисте"""
        if not self.genre_distribution:
            self.analyze_genre_distribution()

        if self.genre_distribution:
            return max(self.genre_distribution, key=self.genre_distribution.get)
        return "Unknown"

    def get_statistics_summary(self) -> Dict:
        """Возвращает сводку статистики плейлиста"""
        return {
            'total_songs': len(self.playlist.songs),
            'total_duration': self.calculate_total_duration(),
            'most_common_genre': self.get_most_common_genre(),
            'genre_count': len(self.analyze_genre_distribution())
        }