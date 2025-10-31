from typing import List, Dict, Optional
from datetime import datetime
from models.playlist_models import Playlist, SmartPlaylist
from exceptions.playlist_exceptions import PlaylistEmptyException


class PlaylistManager:
    def create_playlist(self, name: str, creator) -> Playlist:
        return Playlist(f"pl_{datetime.now().timestamp()}", name, creator)

    def delete_playlist(self, playlist: Playlist) -> bool:
        return True

    def rename_playlist(self, playlist: Playlist, new_name: str) -> bool:
        playlist.name = new_name
        return True

    def duplicate_playlist(self, playlist: Playlist) -> Playlist:
        new_playlist = Playlist(
            f"pl_{datetime.now().timestamp()}",
            f"{playlist.name} (Copy)",
            playlist.creator
        )
        new_playlist.songs = playlist.songs.copy()
        return new_playlist

    def export_playlist(self, playlist: Playlist, format: str) -> str:
        return f"Exported playlist: {playlist.name}"

    def import_playlist(self, file_path: str, creator) -> Playlist:
        return Playlist(f"pl_{datetime.now().timestamp()}", "Imported Playlist", creator)

    def merge_playlists(self, playlists: List[Playlist]) -> Playlist:
        merged = Playlist(f"pl_{datetime.now().timestamp()}", "Merged Playlist", playlists[0].creator)
        for pl in playlists:
            merged.songs.extend(pl.songs)
        return merged

    def sort_playlist(self, playlist: Playlist, criteria: str) -> bool:
        if criteria == "title":
            playlist.songs.sort(key=lambda x: x.title)
        return True

    def shuffle_playlist(self, playlist: Playlist) -> bool:
        import random
        random.shuffle(playlist.songs)
        return True

    def filter_playlist(self, playlist: Playlist, criteria: dict) -> List:
        return [song for song in playlist.songs if self._matches_criteria(song, criteria)]

    def _matches_criteria(self, song, criteria: dict) -> bool:
        return True


class SmartPlaylistGenerator:
    def generate_by_genre(self, genre: str, library, max_songs: int) -> SmartPlaylist:
        criteria = {'genre': genre, 'max_songs': max_songs}
        return SmartPlaylist(f"spl_{datetime.now().timestamp()}", f"{genre} Mix", None, criteria)

    def generate_by_mood(self, mood: str, library, max_songs: int) -> SmartPlaylist:
        criteria = {'mood': mood, 'max_songs': max_songs}
        return SmartPlaylist(f"spl_{datetime.now().timestamp()}", f"{mood} Mood", None, criteria)

    def generate_by_decade(self, decade: int, library, max_songs: int) -> SmartPlaylist:
        criteria = {'decade': decade, 'max_songs': max_songs}
        return SmartPlaylist(f"spl_{datetime.now().timestamp()}", f"{decade}s Hits", None, criteria)

    def generate_by_artist(self, artist: str, library, max_songs: int) -> SmartPlaylist:
        criteria = {'artist': artist, 'max_songs': max_songs}
        return SmartPlaylist(f"spl_{datetime.now().timestamp()}", f"{artist} Collection", None, criteria)

    def generate_recommendations(self, user, library, max_songs: int) -> SmartPlaylist:
        criteria = {'recommendations': True, 'max_songs': max_songs}
        return SmartPlaylist(f"spl_{datetime.now().timestamp()}", "Recommended for You", user, criteria)

    def update_smart_playlist(self, playlist: SmartPlaylist) -> bool:
        return True


class PlaylistAnalyzer:
    def calculate_total_duration(self, playlist: Playlist) -> float:
        return sum(song.duration for song in playlist.songs)

    def get_genre_distribution(self, playlist: Playlist) -> Dict:
        distribution = {}
        for song in playlist.songs:
            distribution[song.genre] = distribution.get(song.genre, 0) + 1
        return distribution

    def find_duplicates(self, playlist: Playlist) -> List:
        seen = set()
        duplicates = []
        for song in playlist.songs:
            if song.title in seen:
                duplicates.append(song)
            seen.add(song.title)
        return duplicates

    def analyze_playlist_energy(self, playlist: Playlist) -> float:
        return sum(song.bpm for song in playlist.songs) / len(playlist.songs) if playlist.songs else 0

    def get_most_common_artist(self, playlist: Playlist) -> str:
        artists = {}
        for song in playlist.songs:
            artists[song.artist] = artists.get(song.artist, 0) + 1
        return max(artists, key=artists.get) if artists else "Unknown"