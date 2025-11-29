from typing import Dict
from .AudioFile import AudioFile

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

    def get_formatted_duration(self) -> str:
        """Возвращает длительность в формате MM:SS"""
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def is_in_tempo_range(self, min_bpm: float, max_bpm: float) -> bool:
        """Проверяет, попадает ли песня в диапазон BPM"""
        return min_bpm <= self.bpm <= max_bpm

    def has_lyrics(self) -> bool:
        """Проверяет, есть ли текст песни"""
        return bool(self.lyrics and self.lyrics.strip())

    def get_metadata_summary(self) -> Dict:
        """Возвращает краткую метаинформацию о песне"""
        return {
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.get_formatted_duration(),
            'genre': self.genre,
            'year': self.year,
            'bpm': self.bpm
        }

    def set_lyrics(self, lyrics: str) -> None:
        """Устанавливает текст песни с валидацией"""
        if lyrics and len(lyrics) > 10:  # Минимальная длина текста
            self.lyrics = lyrics

    def is_similar_genre(self, other_song: 'Song') -> bool:
        """Проверяет, похожи ли жанры песен"""
        return self.genre.lower() == other_song.genre.lower()