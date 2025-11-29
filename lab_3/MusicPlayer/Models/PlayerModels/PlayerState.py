
class PlayerState:
    def __init__(self):
        self.current_song = None
        self.is_playing = False
        self.current_time = 0
        self.volume = 50
        self.repeat_mode = "none"
        self.shuffle = False
        self.playback_speed = 1.0

    def get_formatted_time(self) -> str:
        """Возвращает текущее время в формате MM:SS"""
        minutes = int(self.current_time // 60)
        seconds = int(self.current_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def set_volume(self, volume: int) -> bool:
        """Устанавливает громкость с проверкой диапазона"""
        if 0 <= volume <= 100:
            self.volume = volume
            return True
        return False

    def adjust_volume(self, delta: int) -> bool:
        """Изменяет громкость на указанное значение"""
        new_volume = self.volume + delta
        return self.set_volume(new_volume)

    def is_repeat_enabled(self) -> bool:
        """Проверяет, включен ли режим повтора"""
        return self.repeat_mode in ["one", "all"]

    def get_playback_info(self) -> dict:
        """Возвращает информацию о состоянии воспроизведения"""
        return {
            'is_playing': self.is_playing,
            'current_time': self.get_formatted_time(),
            'volume': self.volume,
            'repeat_mode': self.repeat_mode,
            'shuffle': self.shuffle,
            'playback_speed': self.playback_speed
        }