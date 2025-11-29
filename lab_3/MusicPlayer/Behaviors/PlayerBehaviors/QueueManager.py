from Models.AudioModels.Song import Song
from Models.PlayerModels.PlaybackQueue import PlaybackQueue
from Models.PlaylistModels.Playlist import Playlist
from Models.UserModels.User import User
from datetime import datetime
from typing import Optional


class QueueManager:
    def __init__(self):
        self.queue = PlaybackQueue()

    def add_to_queue(self, song: Song) -> bool:
        """Добавляет песню в очередь"""
        self.queue.songs.append(song)
        return True

    def add_to_queue_next(self, song: Song) -> bool:
        """Добавляет песню следующей в очереди"""
        if self.queue.current_index < len(self.queue.songs):
            self.queue.songs.insert(self.queue.current_index + 1, song)
        else:
            self.queue.songs.append(song)
        return True

    def remove_from_queue(self, song: Song) -> bool:
        """Удаляет песню из очереди"""
        if song in self.queue.songs:
            # Если удаляем текущую играющую песню, переходим к следующей
            if (self.queue.current_index < len(self.queue.songs) and
                    self.queue.songs[self.queue.current_index] == song):
                self.queue.current_index = min(self.queue.current_index, len(self.queue.songs) - 2)

            self.queue.songs.remove(song)
            return True
        return False

    def clear_queue(self) -> bool:
        """Очищает очередь"""
        self.queue.songs.clear()
        self.queue.current_index = 0
        self.queue.history.clear()
        return True

    def move_in_queue(self, old_index: int, new_index: int) -> bool:
        """Перемещает песню в очереди"""
        if (0 <= old_index < len(self.queue.songs) and
                0 <= new_index < len(self.queue.songs)):

            # Корректируем текущий индекс если он затронут перемещением
            if self.queue.current_index == old_index:
                self.queue.current_index = new_index
            elif old_index < self.queue.current_index <= new_index:
                self.queue.current_index -= 1
            elif new_index <= self.queue.current_index < old_index:
                self.queue.current_index += 1

            song = self.queue.songs.pop(old_index)
            self.queue.songs.insert(new_index, song)
            return True
        return False

    def save_queue_as_playlist(self, name: str, creator: User) -> Playlist:
        """Сохраняет текущую очередь как плейлист"""
        if not self.queue.songs:
            raise ValueError("Cannot save empty queue as playlist")

        if not name:
            name = f"Queue {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        # Создаем новый плейлист
        playlist_id = f"pl_{int(datetime.now().timestamp())}"
        playlist = Playlist(playlist_id, name, creator)

        # Копируем песни из очереди в плейлист
        playlist.songs = self.queue.songs.copy()
        playlist.description = f"Saved from queue on {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        return playlist

    def get_current_song(self) -> Optional[Song]:
        """Возвращает текущую играющую песню"""
        if (self.queue.songs and
                0 <= self.queue.current_index < len(self.queue.songs)):
            return self.queue.songs[self.queue.current_index]
        return None

    def get_next_song(self) -> Optional[Song]:
        """Возвращает следующую песню в очереди"""
        if not self.queue.songs:
            return None

        next_index = (self.queue.current_index + 1) % len(self.queue.songs)
        return self.queue.songs[next_index]

    def get_previous_song(self) -> Optional[Song]:
        """Возвращает предыдущую песню в очереди"""
        if not self.queue.songs or not self.queue.history:
            return None

        return self.queue.history[-1] if self.queue.history else None

    def get_queue_length(self) -> int:
        """Возвращает количество песен в очереди"""
        return len(self.queue.songs)

    def get_queue_duration(self) -> int:
        """Возвращает общую длительность очереди в секундах"""
        return sum(song.duration for song in self.queue.songs)

    def get_remaining_duration(self) -> int:
        """Возвращает оставшуюся длительность очереди от текущей позиции"""
        if not self.queue.songs:
            return 0

        remaining_songs = self.queue.songs[self.queue.current_index:]
        return sum(song.duration for song in remaining_songs)

    def shuffle_queue(self) -> bool:
        """Перемешивает очередь, сохраняя текущую песню на месте"""
        if len(self.queue.songs) <= 1:
            return True

        current_song = self.get_current_song()

        # Перемешиваем все песни кроме текущей
        songs_to_shuffle = [s for s in self.queue.songs if s != current_song]
        import random
        random.shuffle(songs_to_shuffle)

        # Вставляем текущую песню обратно на ее позицию
        if current_song:
            songs_to_shuffle.insert(self.queue.current_index, current_song)

        self.queue.songs = songs_to_shuffle
        return True

    def get_queue_info(self) -> dict:
        """Возвращает информацию об очереди"""
        current_song = self.get_current_song()
        return {
            'total_songs': len(self.queue.songs),
            'current_position': self.queue.current_index + 1,
            'current_song': current_song.title if current_song else None,
            'total_duration': self.get_queue_duration(),
            'remaining_duration': self.get_remaining_duration(),
            'history_size': len(self.queue.history)
        }