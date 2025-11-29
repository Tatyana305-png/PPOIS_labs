import os
from typing import List
from Models.AudioModels.Song import Song
from Exceptions.AudioCorruptedException import AudioCorruptedException
from .AudioFileManager import AudioFileManager

class AudioAnalyzer:
    def analyze_bpm(self, audio_file: Song) -> float:
        """Анализирует BPM (темп) аудиофайла с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot analyze BPM of invalid audio file")

        if hasattr(audio_file, 'bpm') and audio_file.bpm > 0:
            return audio_file.bpm
        return 120.0  # Значение по умолчанию

    def detect_key(self, audio_file: Song) -> str:
        """Определяет музыкальный ключ аудиофайла с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot detect key of invalid audio file")

        if hasattr(audio_file, 'key') and audio_file.key:
            return audio_file.key
        return "C"  # Значение по умолчанию

    def analyze_loudness(self, audio_file: Song) -> float:
        """Анализирует громкость аудиофайла с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot analyze loudness of invalid audio file")

        return -10.0  # LUFS

    def detect_silence(self, audio_file: Song) -> List[tuple]:
        """Обнаруживает тихие участки в аудиофайле с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot detect silence in invalid audio file")

        return []

    def extract_waveform(self, audio_file: Song) -> List[float]:
        """Извлекает waveform данные с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot extract waveform from invalid audio file")

        return [0.0] * 100  # Упрощенный waveform

    def analyze_frequency_spectrum(self, audio_file: Song) -> dict:
        """Анализирует частотный спектр с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot analyze frequency spectrum of invalid audio file")

        return {
            'low': 25.0,
            'mid_low': 15.0,
            'mid': 10.0,
            'mid_high': 8.0,
            'high': 5.0
        }

    def detect_bpm_changes(self, audio_file: Song) -> List[float]:
        """Обнаруживает изменения BPM в течение трека с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot detect BPM changes in invalid audio file")

        base_bpm = self.analyze_bpm(audio_file)
        return [base_bpm]  # В реальном приложении здесь были бы изменения

    def analyze_audio_quality(self, audio_file: Song) -> dict:
        """Анализирует качество аудио с проверкой"""
        manager = AudioFileManager()
        if not manager.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot analyze quality of invalid audio file")

        return {
            'score': 85,
            'bitrate_quality': 'good',
            'dynamic_range': 'medium',
            'clipping_detected': False,
            'issues': []
        }