import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.LibraryModels.Genre import Genre

class TestGenre(unittest.TestCase):

    def setUp(self):
        self.genre = Genre("gen123", "Rock")

    def test_genre_initialization(self):
        """Тест инициализации жанра"""
        self.assertEqual(self.genre.genre_id, "gen123")
        self.assertEqual(self.genre.name, "Rock")
        self.assertEqual(self.genre.description, "")
        self.assertEqual(self.genre.origin, "")
        self.assertEqual(self.genre.era, "")
        self.assertEqual(self.genre.related_genres, [])

    def test_genre_description(self):
        """Тест описания жанра"""
        description = "Rock music is a broad genre of popular music that originated as 'rock and roll' in the United States in the late 1940s and early 1950s."
        self.genre.description = description

        self.assertEqual(self.genre.description, description)
        self.assertIn("rock and roll", self.genre.description)

    def test_genre_origin(self):
        """Тест происхождения жанра"""
        origins = ["United States", "United Kingdom", "Jamaica", "Brazil", "Japan"]

        for origin in origins:
            self.genre.origin = origin
            self.assertEqual(self.genre.origin, origin)

    def test_genre_era(self):
        """Тест эры жанра"""
        eras = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s"]

        for era in eras:
            self.genre.era = era
            self.assertEqual(self.genre.era, era)

    def test_genre_related_genres(self):
        """Тест связанных жанров"""
        related_genres = ["Hard Rock", "Alternative Rock", "Punk Rock", "Grunge"]
        self.genre.related_genres = related_genres

        self.assertEqual(len(self.genre.related_genres), 4)
        self.assertIn("Hard Rock", self.genre.related_genres)
        self.assertIn("Alternative Rock", self.genre.related_genres)
        self.assertIn("Punk Rock", self.genre.related_genres)
        self.assertIn("Grunge", self.genre.related_genres)

        # Добавляем новый связанный жанр
        self.genre.related_genres.append("Progressive Rock")
        self.assertEqual(len(self.genre.related_genres), 5)
        self.assertIn("Progressive Rock", self.genre.related_genres)


if __name__ == '__main__':
    unittest.main()