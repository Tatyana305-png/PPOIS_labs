from datetime import datetime
from .AudioFile import AudioFile
from typing import Dict

class Podcast(AudioFile):
    def __init__(self, file_path: str, title: str, duration: float, host: str, episode: int):
        super().__init__(file_path, title, duration)
        self.host = host
        self.episode = episode
        self.guest = ""
        self.topic = ""
        self.publication_date = datetime.now()
        self.description = ""

    def is_published(self) -> bool:
        """Проверяет, опубликован ли подкаст"""
        return self.publication_date <= datetime.now()

    def has_guest(self) -> bool:
        """Проверяет, есть ли гость в выпуске"""
        return bool(self.guest and self.guest.strip())

    def get_episode_info(self) -> Dict:
        """Возвращает информацию о выпуске"""
        return {
            'episode': self.episode,
            'host': self.host,
            'guest': self.guest,
            'topic': self.topic,
            'publication_date': self.publication_date.strftime("%Y-%m-%d")
        }

    def set_guest(self, guest_name: str) -> None:
        """Устанавливает имя гостя"""
        if guest_name and guest_name.strip():
            self.guest = guest_name.strip()

    def is_recent(self, days: int = 30) -> bool:
        """Проверяет, является ли выпуск недавним"""
        delta = datetime.now() - self.publication_date
        return delta.days <= days