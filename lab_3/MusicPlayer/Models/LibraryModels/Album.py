from datetime import datetime
from .Artist import Artist

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

    def set_release_date(self, year: int, month: int, day: int) -> None:
        """Устанавливает дату выпуска"""
        try:
            self.release_date = datetime(year, month, day)
        except ValueError:
            pass

    def is_recent(self, months: int = 6) -> bool:
        """Проверяет, является ли альбом недавним"""
        delta = datetime.now() - self.release_date
        return delta.days <= months * 30

    def get_formatted_duration(self) -> str:
        """Возвращает длительность в формате HH:MM:SS"""
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        seconds = int(self.duration % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def matches_artist(self, artist_name: str) -> bool:
        """Проверяет, совпадает ли артист альбома"""
        return self.artist.name.lower() == artist_name.lower()