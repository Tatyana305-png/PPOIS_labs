class PlayerSettings:
    def __init__(self):
        self.audio_device = None
        self.volume_normalization = False
        self.gapless_playback = True
        self.crossfade_duration = 0
        self.high_quality_streaming = True
        self.download_quality = "high"

    def enable_volume_normalization(self) -> None:
        """Включает нормализацию громкости"""
        self.volume_normalization = True

    def disable_volume_normalization(self) -> None:
        """Выключает нормализацию громкости"""
        self.volume_normalization = False

    def set_crossfade(self, duration: int) -> bool:
        """Устанавливает длительность кроссфейда"""
        if 0 <= duration <= 10:
            self.crossfade_duration = duration
            return True
        return False

    def set_download_quality(self, quality: str) -> bool:
        """Устанавливает качество загрузки"""
        valid_qualities = ["low", "medium", "high", "very_high"]
        if quality in valid_qualities:
            self.download_quality = quality
            return True
        return False

    def get_audio_settings(self) -> dict:
        """Возвращает текущие аудио-настройки"""
        return {
            'volume_normalization': self.volume_normalization,
            'gapless_playback': self.gapless_playback,
            'crossfade_duration': f"{self.crossfade_duration}s",
            'high_quality_streaming': self.high_quality_streaming,
            'download_quality': self.download_quality
        }