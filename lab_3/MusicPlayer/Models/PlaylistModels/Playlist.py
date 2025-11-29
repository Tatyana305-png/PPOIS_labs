from datetime import datetime
from Exceptions.DuplicateSongException import DuplicateSongException
from Exceptions.PlaylistEmptyException import PlaylistEmptyException


class Playlist:
    def __init__(self, playlist_id: str, name: str, creator):
        self.playlist_id = playlist_id
        self.name = name
        self.creator = creator
        self.songs = []
        self.creation_date = datetime.now()
        self.description = ""
        self.cover_art = ""
        self.is_public = False
        self.play_count = 0
        self.last_played = None

    def add_song(self, song):
        if song in self.songs:
            raise DuplicateSongException("Song already in playlist")
        self.songs.append(song)

    def remove_song(self, song):
        if not self.songs:
            raise PlaylistEmptyException("Playlist is empty")
        if song in self.songs:
            self.songs.remove(song)
        else:
            raise ValueError("Song not found in playlist")

    def get_total_duration(self) -> int:
        """Возвращает общую длительность плейлиста в секундах"""
        return sum(song.duration for song in self.songs) if self.songs else 0

    def get_song_count(self) -> int:
        """Возвращает количество песен в плейлисте"""
        return len(self.songs)

    def clear_playlist(self) -> None:
        """Очищает плейлист"""
        self.songs.clear()

    def contains_song(self, song) -> bool:
        """Проверяет, содержится ли песня в плейлисте"""
        return song in self.songs

    def play(self) -> None:
        """Увеличивает счетчик проигрываний"""
        self.play_count += 1
        self.last_played = datetime.now()