from datetime import datetime
from typing import List, Optional
from exceptions.audio_exceptions import InvalidAudioFormatException


class AudioFile:
    def __init__(self, file_path: str, title: str, duration: float):
        self.file_path = file_path
        self.title = title
        self.duration = duration
        self.file_size = 0
        self.bitrate = 320
        self.sample_rate = 44100
        self.channels = 2
        self.format = "mp3"
        self.creation_date = datetime.now()
        self.modification_date = datetime.now()

    def validate_format(self):
        if self.format not in ["mp3", "wav", "flac", "aac"]:
            raise InvalidAudioFormatException(f"Unsupported format: {self.format}")


class Song(AudioFile):
    def __init__(self, file_path: str, title: str, duration: float, artist: str, album: str):
        super().__init__(file_path, title, duration)
        self.artist = artist
        self.album = album
        self.genre = "Unknown"
        self.year = 2024
        self.track_number = 1
        self.lyrics = ""
        self.composer = ""
        self.bpm = 120
        self.key = "C"


class Podcast(AudioFile):
    def __init__(self, file_path: str, title: str, duration: float, host: str, episode: int):
        super().__init__(file_path, title, duration)
        self.host = host
        self.episode = episode
        self.guest = ""
        self.topic = ""
        self.publication_date = datetime.now()
        self.description = ""


class Audiobook(AudioFile):
    def __init__(self, file_path: str, title: str, duration: float, author: str, narrator: str):
        super().__init__(file_path, title, duration)
        self.author = author
        self.narrator = narrator
        self.chapter = 1
        self.total_chapters = 10
        self.publisher = ""
        self.isbn = ""


class AudioMetadata:
    def __init__(self):
        self.id3_tags = {}
        self.artwork = None
        self.copyright = ""
        self.encoder = ""
        self.comments = ""


class AudioQuality:
    def __init__(self):
        self.bit_depth = 16
        self.dynamic_range = 0
        self.frequency_response = ""
        self.signal_noise_ratio = 0