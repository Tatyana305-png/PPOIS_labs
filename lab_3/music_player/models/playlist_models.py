from datetime import datetime
from typing import List, Optional
from exceptions.playlist_exceptions import PlaylistEmptyException, DuplicateSongException


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
        self.songs.remove(song)


class SmartPlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, creator, criteria: dict):
        super().__init__(playlist_id, name, creator)
        self.criteria = criteria
        self.auto_update = True
        self.update_frequency = "daily"
        self.max_songs = 100


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, creator):
        super().__init__(playlist_id, name, creator)
        self.collaborators = []
        self.edit_permissions = "all"
        self.approval_required = False


class PlaylistFolder:
    def __init__(self, folder_id: str, name: str, owner):
        self.folder_id = folder_id
        self.name = name
        self.owner = owner
        self.playlists = []
        self.description = ""
        self.creation_date = datetime.now()


class PlaylistStatistics:
    def __init__(self, playlist: Playlist):
        self.playlist = playlist
        self.total_duration = 0
        self.avg_rating = 0
        self.genre_distribution = {}
        self.most_played_song = None