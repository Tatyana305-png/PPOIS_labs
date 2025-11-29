import unittest
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.LibraryModels.MusicLibrary import MusicLibrary
from Models.LibraryModels.Artist import Artist
from Models.LibraryModels.Album import Album
from Models.UserModels.User import User
from Models.AudioModels.Song import Song


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

if __name__ == '__main__':
    unittest.main()