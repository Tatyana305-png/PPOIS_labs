from typing import Dict

class PlaylistAnalyzer:
    def calculate_total_duration(self, playlist) -> int:
        """Вычисляет общую длительность плейлиста"""
        return sum(song.duration for song in playlist.songs)

    def get_genre_distribution(self, playlist) -> Dict[str, int]:
        """Возвращает распределение по жанрам"""
        distribution = {}
        for song in playlist.songs:
            if hasattr(song, 'genre'):
                distribution[song.genre] = distribution.get(song.genre, 0) + 1
        return distribution

    def find_duplicates(self, playlist) -> list:
        """Находит дубликаты песен в плейлисте"""
        seen = set()
        duplicates = []
        for song in playlist.songs:
            if song in seen:
                duplicates.append(song)
            else:
                seen.add(song)
        return duplicates

    def analyze_playlist_energy(self, playlist) -> float:
        """Анализирует энергию плейлиста (средний BPM)"""
        total_bpm = 0
        count = 0
        for song in playlist.songs:
            if hasattr(song, 'bpm') and song.bpm:
                total_bpm += song.bpm
                count += 1
        return total_bpm / count if count > 0 else 0

    def get_most_common_artist(self, playlist) -> str:
        """Возвращает самого частого артиста"""
        artists = {}
        for song in playlist.songs:
            if hasattr(song, 'artist'):
                artists[song.artist] = artists.get(song.artist, 0) + 1
        return max(artists.items(), key=lambda x: x[1])[0] if artists else ""