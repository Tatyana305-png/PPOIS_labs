from typing import List

class Genre:
    def __init__(self, genre_id: str, name: str):
        self.genre_id = genre_id
        self.name = name
        self.description = ""
        self.origin = ""
        self.era = ""
        self.related_genres = []

    def add_related_genre(self, genre: 'Genre') -> None:
        """Добавляет связанный жанр"""
        if genre and genre not in self.related_genres:
            self.related_genres.append(genre)

    def is_related_to(self, genre_name: str) -> bool:
        """Проверяет, связан ли жанр с указанным"""
        return any(g.name.lower() == genre_name.lower() for g in self.related_genres)

    def get_related_genre_names(self) -> List[str]:
        """Возвращает названия связанных жанров"""
        return [genre.name for genre in self.related_genres]

    def has_description(self) -> bool:
        """Проверяет, есть ли описание жанра"""
        return bool(self.description and self.description.strip())