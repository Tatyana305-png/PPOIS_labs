from datetime import datetime
from typing import Dict, List
from .User import User

class ListeningHistory:
    def __init__(self, user: User):
        self.user = user
        self.entries = []
        self.total_listening_time = 0
        self.most_played_songs = []

    def add_entry(self, song, duration: float) -> None:
        """Добавляет запись в историю прослушивания"""
        if song and duration > 0:
            self.entries.append({
                'song': song,
                'timestamp': datetime.now(),
                'duration': duration
            })
            self.total_listening_time += duration

    def get_recent_entries(self, count: int = 10) -> List:
        """Возвращает последние записи прослушивания"""
        return self.entries[-count:] if self.entries else []

    def get_total_listening_hours(self) -> float:
        """Возвращает общее время прослушивания в часах"""
        return self.total_listening_time / 3600

    def clear_history(self) -> None:
        """Очищает историю прослушивания"""
        self.entries.clear()
        self.total_listening_time = 0

    def get_history_summary(self) -> Dict:
        """Возвращает сводку истории прослушивания"""
        return {
            'total_entries': len(self.entries),
            'total_listening_hours': round(self.get_total_listening_hours(), 1),
            'most_played_count': len(self.most_played_songs)
        }