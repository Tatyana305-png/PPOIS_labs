from datetime import datetime
from typing import List, Dict

class MusicLibrary:
    def __init__(self, owner):
        self.owner = owner
        self.songs = []
        self.artists = []
        self.albums = []
        self.playlists = []
        self.total_size = 0
        self.last_updated = datetime.now()
        self.import_sources = []

    def add_song(self, song) -> bool:
        """Добавляет песню в библиотеку"""
        if song and song not in self.songs:
            self.songs.append(song)
            self._update_library_state()
            return True
        return False

    def remove_song(self, song) -> bool:
        """Удаляет песню из библиотеки"""
        if song in self.songs:
            self.songs.remove(song)
            self._update_library_state()
            return True
        return False

    def get_songs_by_artist(self, artist_name: str) -> List:
        """Возвращает песни указанного артиста"""
        return [song for song in self.songs if song.artist == artist_name]

    def get_library_stats(self) -> Dict:
        """Возвращает статистику библиотеки"""
        return {
            'total_songs': len(self.songs),
            'total_artists': len(self.artists),
            'total_albums': len(self.albums),
            'total_playlists': len(self.playlists),
            'total_size_gb': round(self.total_size / (1024 ** 3), 2)
        }

    def _update_library_state(self) -> None:
        """Обновляет состояние библиотеки"""
        self.total_size = sum(getattr(song, 'file_size', 0) for song in self.songs)
        self.last_updated = datetime.now()