from datetime import datetime
from typing import List
from Models.PlaylistModels.SmartPlaylist import SmartPlaylist
from Models.LibraryModels.MusicLibrary import MusicLibrary

class SmartPlaylistGenerator:
    def generate_by_criteria(self, criteria: dict, library: MusicLibrary, max_songs: int) -> SmartPlaylist:
        """Создает умный плейлист по заданным критериям"""
        if not criteria or max_songs <= 0:
            raise ValueError("Invalid criteria or max_songs")

        filtered_songs = self._filter_songs_by_criteria(library.songs, criteria)
        selected_songs = filtered_songs[:max_songs]

        playlist_name = self._generate_playlist_name(criteria)
        playlist = SmartPlaylist(
            f"spl_{int(datetime.now().timestamp())}",
            playlist_name,
            criteria.get('user'),
            criteria
        )
        playlist.songs = selected_songs
        return playlist

    def generate_by_genre(self, genre: str, library: MusicLibrary, max_songs: int) -> SmartPlaylist:
        """Создает умный плейлист по жанру"""
        criteria = {'genre': genre, 'max_songs': max_songs}
        return self.generate_by_criteria(criteria, library, max_songs)

    def _filter_songs_by_criteria(self, songs: List, criteria: dict) -> List:
        """Фильтрует песни по критериям"""
        filtered = songs

        if 'genre' in criteria:
            genre = criteria['genre']
            filtered = [s for s in filtered if hasattr(s, 'genre') and s.genre == genre]

        if 'artist' in criteria:
            artist = criteria['artist']
            filtered = [s for s in filtered if hasattr(s, 'artist') and s.artist == artist]

        if 'min_bpm' in criteria and 'max_bpm' in criteria:
            min_bpm, max_bpm = criteria['min_bpm'], criteria['max_bpm']
            filtered = [s for s in filtered if hasattr(s, 'bpm') and min_bpm <= s.bpm <= max_bpm]

        return filtered

    def _generate_playlist_name(self, criteria: dict) -> str:
        """Генерирует название плейлиста на основе критериев"""
        if 'name' in criteria:
            return criteria['name']

        if 'genre' in criteria:
            return f"{criteria['genre']} Mix"

        if 'artist' in criteria:
            return f"{criteria['artist']} Collection"

        return "Smart Playlist"