from typing import Dict

class UserPreferences:
    def __init__(self):
        self.audio_quality = "high"
        self.auto_play = True
        self.crossfade_duration = 0
        self.equalizer_preset = "flat"
        self.replay_gain = False
        self.volume_limit = 100
        self.keyboard_shortcuts = {}

    def set_audio_quality(self, quality: str) -> bool:
        """Устанавливает качество аудио"""
        valid_qualities = ["low", "medium", "high", "very_high"]
        if quality in valid_qualities:
            self.audio_quality = quality
            return True
        return False

    def set_crossfade(self, duration: int) -> bool:
        """Устанавливает длительность кроссфейда"""
        if 0 <= duration <= 10:
            self.crossfade_duration = duration
            return True
        return False

    def set_volume_limit(self, limit: int) -> bool:
        """Устанавливает лимит громкости"""
        if 0 <= limit <= 100:
            self.volume_limit = limit
            return True
        return False

    def add_keyboard_shortcut(self, action: str, shortcut: str) -> None:
        """Добавляет клавиатурное сокращение"""
        if action and shortcut:
            self.keyboard_shortcuts[action] = shortcut

    def get_playback_settings(self) -> Dict:
        """Возвращает настройки воспроизведения"""
        return {
            'audio_quality': self.audio_quality,
            'auto_play': self.auto_play,
            'crossfade_duration': self.crossfade_duration,
            'equalizer_preset': self.equalizer_preset,
            'volume_limit': self.volume_limit
        }