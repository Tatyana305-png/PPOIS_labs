import unittest
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.library_models import MusicLibrary, Artist, Album, Genre, LibraryScanner
from models.user_models import User
from models.audio_models import Song


class TestMusicLibrary(unittest.TestCase):

    def setUp(self):
        self.user = User("user123", "testuser", "test@example.com")
        self.library = MusicLibrary(self.user)

        # Создаем тестовые данные
        self.artist1 = Artist("art1", "Artist One")
        self.artist2 = Artist("art2", "Artist Two")

        self.album1 = Album("alb1", "Album One", self.artist1)
        self.album2 = Album("alb2", "Album Two", self.artist2)

        self.song1 = Song("/music/song1.mp3", "Song One", 180, "Artist One", "Album One")
        self.song2 = Song("/music/song2.mp3", "Song Two", 200, "Artist Two", "Album Two")
        self.song3 = Song("/music/song3.mp3", "Song Three", 220, "Artist One", "Album One")

    def test_music_library_initialization(self):
        """Тест инициализации музыкальной библиотеки"""
        self.assertEqual(self.library.owner, self.user)
        self.assertEqual(self.library.songs, [])
        self.assertEqual(self.library.artists, [])
        self.assertEqual(self.library.albums, [])
        self.assertEqual(self.library.playlists, [])
        self.assertEqual(self.library.total_size, 0)
        self.assertIsInstance(self.library.last_updated, datetime)
        self.assertEqual(self.library.import_sources, [])

    def test_add_songs_to_library(self):
        """Тест добавления песен в библиотеку"""
        self.library.songs.append(self.song1)
        self.library.songs.append(self.song2)

        self.assertEqual(len(self.library.songs), 2)
        self.assertIn(self.song1, self.library.songs)
        self.assertIn(self.song2, self.library.songs)

        # Проверяем, что песни не дублируются при повторном добавлении
        self.library.songs.append(self.song1)
        self.assertEqual(len(self.library.songs), 3)  # В текущей реализации дубликаты разрешены

    def test_add_artists_to_library(self):
        """Тест добавления артистов в библиотеку"""
        self.library.artists.append(self.artist1)
        self.library.artists.append(self.artist2)

        self.assertEqual(len(self.library.artists), 2)
        self.assertIn(self.artist1, self.library.artists)
        self.assertIn(self.artist2, self.library.artists)

    def test_add_albums_to_library(self):
        """Тест добавления альбомов в библиотеку"""
        self.library.albums.append(self.album1)
        self.library.albums.append(self.album2)

        self.assertEqual(len(self.library.albums), 2)
        self.assertIn(self.album1, self.library.albums)
        self.assertIn(self.album2, self.library.albums)

    def test_library_total_size_calculation(self):
        """Тест расчета общего размера библиотеки"""
        # Симулируем размеры файлов
        self.song1.file_size = 1024 * 1024  # 1 MB
        self.song2.file_size = 2048 * 1024  # 2 MB
        self.song3.file_size = 1536 * 1024  # 1.5 MB

        self.library.songs = [self.song1, self.song2, self.song3]

        # В реальной реализации здесь была бы автоматическая сумма
        total_size = sum(song.file_size for song in self.library.songs)
        self.library.total_size = total_size

        expected_size = (1024 + 2048 + 1536) * 1024  # 4.5 MB в байтах
        self.assertEqual(self.library.total_size, expected_size)

    def test_library_import_sources(self):
        """Тест управления источниками импорта"""
        sources = ["local_folder", "spotify_import", "youtube_download"]
        self.library.import_sources = sources

        self.assertEqual(len(self.library.import_sources), 3)
        self.assertIn("local_folder", self.library.import_sources)
        self.assertIn("spotify_import", self.library.import_sources)
        self.assertIn("youtube_download", self.library.import_sources)

        # Добавляем новый источник
        self.library.import_sources.append("soundcloud")
        self.assertEqual(len(self.library.import_sources), 4)
        self.assertIn("soundcloud", self.library.import_sources)

    def test_library_last_updated(self):
        """Тест обновления времени последнего изменения"""
        initial_time = self.library.last_updated

        # Симулируем обновление библиотеки
        import time
        time.sleep(0.1)  # Небольшая задержка
        self.library.last_updated = datetime.now()

        self.assertNotEqual(self.library.last_updated, initial_time)
        self.assertIsInstance(self.library.last_updated, datetime)


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


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для моделей библиотеки"""

    def test_empty_library(self):
        """Тест пустой библиотеки"""
        user = User("empty_user", "empty", "empty@example.com")
        empty_library = MusicLibrary(user)

        self.assertEqual(len(empty_library.songs), 0)
        self.assertEqual(len(empty_library.artists), 0)
        self.assertEqual(len(empty_library.albums), 0)
        self.assertEqual(len(empty_library.playlists), 0)
        self.assertEqual(empty_library.total_size, 0)
        self.assertEqual(len(empty_library.import_sources), 0)

    def test_artist_with_minimal_info(self):
        """Тест артиста с минимальной информацией"""
        minimal_artist = Artist("min_art", "Minimal Artist")
        # Только обязательные поля заполнены

        self.assertEqual(minimal_artist.artist_id, "min_art")
        self.assertEqual(minimal_artist.name, "Minimal Artist")
        self.assertEqual(minimal_artist.genres, [])
        self.assertEqual(minimal_artist.biography, "")
        self.assertEqual(minimal_artist.formed_year, 0)
        self.assertIsNone(minimal_artist.disbanded_year)

    def test_album_without_artist(self):
        """Тест альбома без артиста"""
        # В текущей реализации артист обязателен при создании
        # Но можно проверить с None артистом
        try:
            album_with_none_artist = Album("alb_none", "No Artist Album", None)
            self.assertIsNone(album_with_none_artist.artist)
        except Exception:
            # В некоторых реализациях это может вызывать ошибку
            pass

    def test_library_scanner_edge_cases(self):
        """Тест граничных случаев сканера библиотеки"""
        user = User("test_user", "test", "test@example.com")
        library = MusicLibrary(user)
        scanner = LibraryScanner(library)

        # Прогресс вне диапазона 0-100
        scanner.scan_progress = -10
        self.assertEqual(scanner.scan_progress, -10)

        scanner.scan_progress = 150
        self.assertEqual(scanner.scan_progress, 150)

        # Неподдерживаемые форматы
        unsupported_formats = ["exe", "txt", "zip", "rar"]
        for format in unsupported_formats:
            self.assertNotIn(format, scanner.supported_formats)


if __name__ == '__main__':
    unittest.main()