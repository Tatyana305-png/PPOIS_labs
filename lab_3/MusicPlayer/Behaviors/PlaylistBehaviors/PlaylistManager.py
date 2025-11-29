from typing import List
from datetime import datetime
from Models.PlaylistModels.Playlist import Playlist


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