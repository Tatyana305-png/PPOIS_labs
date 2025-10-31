from typing import List, Dict
from datetime import datetime


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


class Artist:
    def __init__(self, artist_id: str, name: str):
        self.artist_id = artist_id
        self.name = name
        self.genres = []
        self.biography = ""
        self.website = ""
        self.social_media = {}
        self.formed_year = 0
        self.disbanded_year = None


class Album:
    def __init__(self, album_id: str, title: str, artist: Artist):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_date = datetime.now()
        self.genre = ""
        self.cover_art = ""
        self.label = ""
        self.total_tracks = 0
        self.duration = 0


class Genre:
    def __init__(self, genre_id: str, name: str):
        self.genre_id = genre_id
        self.name = name
        self.description = ""
        self.origin = ""
        self.era = ""
        self.related_genres = []


class LibraryScanner:
    def __init__(self, library: MusicLibrary):
        self.library = library
        self.supported_formats = ["mp3", "wav", "flac", "aac"]
        self.scan_progress = 0
        self.last_scan = None