from .Playlist import Playlist
from typing import Dict


class SmartPlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, creator, criteria: dict):
        super().__init__(playlist_id, name, creator)
        self.criteria = criteria
        self.auto_update = True
        self.update_frequency = "daily"
        self.max_songs = 100

    def meets_criteria(self, song) -> bool:
        """Проверяет, соответствует ли песня критериям плейлиста"""
        if 'genre' in self.criteria and hasattr(song, 'genre'):
            if song.genre != self.criteria['genre']:
                return False

        if 'min_bpm' in self.criteria and hasattr(song, 'bpm'):
            if song.bpm < self.criteria['min_bpm']:
                return False

        if 'max_bpm' in self.criteria and hasattr(song, 'bpm'):
            if song.bpm > self.criteria['max_bpm']:
                return False

        return True

    def should_auto_update(self) -> bool:
        """Проверяет, нужно ли автоматическое обновление"""
        return self.auto_update

    def get_criteria_summary(self) -> Dict:
        """Возвращает сводку критериев плейлиста"""
        return {
            'criteria_count': len(self.criteria),
            'auto_update': self.auto_update,
            'update_frequency': self.update_frequency,
            'max_songs': self.max_songs
        }

    def set_update_frequency(self, frequency: str) -> bool:
        """Устанавливает частоту обновления"""
        valid_frequencies = ["hourly", "daily", "weekly", "monthly"]
        if frequency in valid_frequencies:
            self.update_frequency = frequency
            return True
        return False