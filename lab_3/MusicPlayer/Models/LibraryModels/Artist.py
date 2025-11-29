from datetime import datetime

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

    def add_genre(self, genre: str) -> None:
        """Добавляет жанр к артисту"""
        if genre and genre not in self.genres:
            self.genres.append(genre)

    def remove_genre(self, genre: str) -> bool:
        """Удаляет жанр у артиста"""
        if genre in self.genres:
            self.genres.remove(genre)
            return True
        return False

    def add_social_media(self, platform: str, handle: str) -> None:
        """Добавляет социальную сеть"""
        if platform and handle:
            self.social_media[platform] = handle

    def is_active(self) -> bool:
        """Проверяет, активен ли артист"""
        return self.disbanded_year is None

    def get_career_years(self) -> int:
        """Возвращает количество лет карьеры"""
        if self.formed_year == 0:
            return 0
        end_year = self.disbanded_year or datetime.now().year
        return max(0, end_year - self.formed_year)