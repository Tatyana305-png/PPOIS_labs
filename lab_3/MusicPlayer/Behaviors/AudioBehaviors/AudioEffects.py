import os
from Models.AudioModels.Song import Song
from .AudioFileManager import AudioFileManager

class AudioEffects:
    def apply_reverb(self, audio_file: Song, amount: float) -> bool:
        """Применяет реверберацию с проверкой параметров"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if amount < 0 or amount > 1:
            raise ValueError("Reverb amount must be between 0 and 1")

        print(f"Applying reverb (amount: {amount}) to: {audio_file.title}")
        return True

    def apply_echo(self, audio_file: Song, delay: float) -> bool:
        """Применяет echo эффект с проверкой параметров"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if delay <= 0:
            raise ValueError("Echo delay must be positive")

        print(f"Applying echo (delay: {delay}s) to: {audio_file.title}")
        return True

    def apply_compression(self, audio_file: Song, ratio: float) -> bool:
        """Применяет компрессию с проверкой параметров"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if ratio < 1:
            raise ValueError("Compression ratio must be at least 1")

        print(f"Applying compression (ratio: {ratio}:1) to: {audio_file.title}")
        return True

    def apply_limiter(self, audio_file: Song, threshold: float) -> bool:
        """Применяет лимитер с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        print(f"Applying limiter (threshold: {threshold}dB) to: {audio_file.title}")
        return True

    def apply_equalizer(self, audio_file: Song, eq_settings: dict) -> bool:
        """Применяет эквалайзер с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if not isinstance(eq_settings, dict):
            raise ValueError("EQ settings must be a dictionary")

        print(f"Applying EQ settings to: {audio_file.title}")
        return True

    def change_pitch(self, audio_file: Song, semitones: int) -> bool:
        """Изменяет pitch (тон) с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if abs(semitones) > 24:  # Ограничение диапазона
            raise ValueError("Pitch change too extreme")

        print(f"Changing pitch by {semitones} semitones for: {audio_file.title}")
        return True

    def change_tempo(self, audio_file: Song, factor: float) -> bool:
        """Изменяет темп с проверкой параметров"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        if factor <= 0:
            raise ValueError("Tempo factor must be positive")

        if factor > 4.0 or factor < 0.25:  # Ограничение диапазона
            raise ValueError("Tempo change too extreme")

        print(f"Changing tempo by factor {factor} for: {audio_file.title}")
        return True

    def reverse_audio(self, audio_file: Song) -> bool:
        """Реверсирует аудио с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            return False

        print(f"Reversing audio: {audio_file.title}")
        return True