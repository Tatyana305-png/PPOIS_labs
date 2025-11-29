from datetime import datetime


class User:
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.registration_date = datetime.now()
        self.last_login = datetime.now()
        self.is_active = True
        self.preferences = {}
        self.favorite_genres = []
        self.language = "en"
        self.theme = "dark"

    def update_last_login(self) -> None:
        """Обновляет время последнего входа"""
        self.last_login = datetime.now()

    def add_favorite_genre(self, genre: str) -> bool:
        """Добавляет жанр в избранные"""
        if genre and genre not in self.favorite_genres:
            self.favorite_genres.append(genre)
            return True
        return False

    def set_preference(self, key: str, value) -> None:
        """Устанавливает настройку пользователя"""
        if key:
            self.preferences[key] = value

    def get_preference(self, key: str, default=None):
        """Возвращает настройку пользователя"""
        return self.preferences.get(key, default)

    def get_account_age_days(self) -> int:
        """Возвращает возраст аккаунта в днях"""
        return (datetime.now() - self.registration_date).days