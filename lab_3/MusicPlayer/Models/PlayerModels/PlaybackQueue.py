class PlaybackQueue:
    def __init__(self):
        self.songs = []
        self.current_index = 0
        self.history = []
        self.up_next = []
        self.max_history_size = 100

    def add_to_queue(self, song) -> bool:
        """Добавляет песню в очередь воспроизведения"""
        if song:
            self.songs.append(song)
            return True
        return False

    def get_current_song(self):
        """Возвращает текущую песню"""
        if self.songs and 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None

    def move_to_next(self) -> bool:
        """Переходит к следующей песне"""
        if self.songs and self.current_index < len(self.songs) - 1:
            # Сохраняем текущую песню в историю
            current_song = self.get_current_song()
            if current_song:
                self.history.append(current_song)
                # Ограничиваем размер истории
                if len(self.history) > self.max_history_size:
                    self.history.pop(0)

            self.current_index += 1
            return True
        return False

    def move_to_previous(self) -> bool:
        """Возвращается к предыдущей песне"""
        if self.history and self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def clear_queue(self) -> None:
        """Очищает очередь воспроизведения"""
        self.songs.clear()
        self.current_index = 0

    def get_queue_info(self) -> dict:
        """Возвращает информацию об очереди"""
        return {
            'total_songs': len(self.songs),
            'current_position': self.current_index + 1,
            'history_size': len(self.history),
            'up_next_count': len(self.up_next)
        }