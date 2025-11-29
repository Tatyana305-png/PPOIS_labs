from datetime import datetime
from typing import Dict
from .User import User

class UserProfile:
    def __init__(self, user: User):
        self.user = user
        self.first_name = ""
        self.last_name = ""
        self.birth_date = None
        self.country = ""
        self.city = ""
        self.bio = ""
        self.avatar_url = ""
        self.social_links = {}

    def get_full_name(self) -> str:
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username

    def set_birth_date(self, year: int, month: int, day: int) -> bool:
        """Устанавливает дату рождения"""
        try:
            self.birth_date = datetime(year, month, day)
            return True
        except ValueError:
            return False

    def get_age(self) -> int:
        """Возвращает возраст пользователя"""
        if not self.birth_date:
            return 0
        today = datetime.now()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def add_social_link(self, platform: str, url: str) -> None:
        """Добавляет ссылку на социальную сеть"""
        if platform and url:
            self.social_links[platform] = url

    def get_profile_summary(self) -> Dict:
        """Возвращает сводку профиля"""
        return {
            'full_name': self.get_full_name(),
            'location': f"{self.city}, {self.country}" if self.city and self.country else "Not specified",
            'age': self.get_age(),
            'social_links_count': len(self.social_links)
        }