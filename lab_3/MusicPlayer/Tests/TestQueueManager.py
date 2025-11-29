import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.PlayerBehaviors.QueueManager import QueueManager
from Models.UserModels.User import User
from Models.AudioModels.Song import Song

class TestQueueManager(unittest.TestCase):

    def setUp(self):
        self.queue_manager = QueueManager()
        self.user = User("test_user", "Test User", "test@example.com")  # ДОБАВЬТЕ ЭТУ СТРОКУ

        # Остальной существующий код setUp...
        self.song1 = Song("song1.mp3", "Song 1", 180, "Artist 1", "Album 1")
        self.song2 = Song("song2.mp3", "Song 2", 200, "Artist 2", "Album 2")
        self.song3 = Song("song3.mp3", "Song 3", 220, "Artist 3", "Album 3")

    def test_add_to_queue(self):
        """Тест добавления песни в очередь"""
        result = self.queue_manager.add_to_queue(self.song1)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 1)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)

        # Добавляем еще одну
        result = self.queue_manager.add_to_queue(self.song2)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song2)

    def test_remove_from_queue_existing_song(self):
        """Тест удаления существующей песни из очереди"""
        # Добавляем песни
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        # Удаляем среднюю
        result = self.queue_manager.remove_from_queue(self.song2)
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song3)

    def test_remove_from_queue_nonexistent_song(self):
        """Тест удаления несуществующей песни из очереди"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.remove_from_queue(self.song3)
        self.assertFalse(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 2)

    def test_clear_queue(self):
        """Тест очистки очереди"""
        # Заполняем очередь
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]
        self.queue_manager.queue.current_index = 1
        self.queue_manager.queue.history = [self.song1]

        # Очищаем
        result = self.queue_manager.clear_queue()
        self.assertTrue(result)
        self.assertEqual(len(self.queue_manager.queue.songs), 0)
        # Текущий индекс и история могут сбрасываться или оставаться (зависит от реализации)

    def test_move_in_queue_valid_positions(self):
        """Тест перемещения песни в очереди с валидными позициями"""
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        # Перемещаем песню с позиции 0 на позицию 2
        result = self.queue_manager.move_in_queue(0, 2)
        self.assertTrue(result)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song2)
        self.assertEqual(self.queue_manager.queue.songs[1], self.song3)
        self.assertEqual(self.queue_manager.queue.songs[2], self.song1)

    def test_move_in_queue_invalid_old_index(self):
        """Тест перемещения с невалидным старым индексом"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.move_in_queue(5, 1)  # Невалидный старый индекс
        self.assertFalse(result)
        # Очередь не должна измениться
        self.assertEqual(len(self.queue_manager.queue.songs), 2)
        self.assertEqual(self.queue_manager.queue.songs[0], self.song1)

    def test_move_in_queue_invalid_new_index(self):
        """Тест перемещения с невалидным новым индексом"""
        self.queue_manager.queue.songs = [self.song1, self.song2]

        result = self.queue_manager.move_in_queue(0, 5)  # Невалидный новый индекс
        self.assertFalse(result)

    def test_save_queue_as_playlist(self):
        """Тест сохранения очереди как плейлиста"""
        self.queue_manager.queue.songs = [self.song1, self.song2, self.song3]

        # Добавляем creator в вызов
        result = self.queue_manager.save_queue_as_playlist("Test Playlist", self.user)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()