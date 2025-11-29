import os
from typing import List, Optional
from Models.AudioModels.Song import Song
from Exceptions.AudioFileNotFoundException import AudioFileNotFoundException
from Exceptions.AudioPermissionException import AudioPermissionException
from Exceptions.InvalidAudioFormatException import InvalidAudioFormatException
from Exceptions.AudioCorruptedException import AudioCorruptedException



class AudioFileManager:
    def load_audio_file(self, file_path: str) -> Song:
        """Загружает аудиофайл с проверкой исключений"""
        if not os.path.exists(file_path):
            raise AudioFileNotFoundException(f"File not found: {file_path}")

        if not os.access(file_path, os.R_OK):
            raise AudioPermissionException(f"No read permission for file: {file_path}")

        file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
        if file_extension not in ['mp3', 'wav', 'flac', 'aac']:
            raise InvalidAudioFormatException(f"Unsupported audio format: {file_extension}")

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise AudioCorruptedException(f"Audio file is empty: {file_path}")

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        return Song(file_path, file_name, 240, "Unknown Artist", "Unknown Album")

    def validate_audio_file(self, audio_file: Song) -> bool:
        """Проверяет валидность аудиофайла с исключениями"""
        if not audio_file or not audio_file.file_path:
            raise AudioFileNotFoundException("Audio file path is missing")

        if not os.path.exists(audio_file.file_path):
            raise AudioFileNotFoundException(f"File not found: {audio_file.file_path}")

        if not os.access(audio_file.file_path, os.R_OK):
            raise AudioPermissionException(f"No read permission for file: {audio_file.file_path}")

        file_size = os.path.getsize(audio_file.file_path)
        if file_size == 0:
            raise AudioCorruptedException(f"Audio file is empty: {audio_file.file_path}")

        if audio_file.duration <= 0:
            raise AudioCorruptedException(f"Invalid audio duration: {audio_file.duration}")

        return True

    def get_audio_duration(self, audio_file: Song) -> float:
        """Возвращает длительность аудиофайла с проверкой"""
        if not self.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot get duration from invalid audio file")
        return audio_file.duration

    def extract_metadata(self, audio_file: Song) -> dict:
        """Извлекает метаданные из аудиофайла с проверкой"""
        if not self.validate_audio_file(audio_file):
            raise AudioCorruptedException("Cannot extract metadata from invalid audio file")

        return {
            'title': audio_file.title,
            'artist': audio_file.artist,
            'album': audio_file.album,
            'duration': audio_file.duration,
            'file_path': audio_file.file_path
        }

    def convert_audio_format(self, audio_file: Song, target_format: str) -> bool:
        """Конвертирует аудиофайл в другой формат с проверкой исключений"""
        if not self.validate_audio_file(audio_file):
            return False

        supported_formats = ['mp3', 'wav', 'flac', 'aac']
        if target_format not in supported_formats:
            raise InvalidAudioFormatException(f"Unsupported target format: {target_format}")

        audio_file.format = target_format
        return True

    def normalize_audio(self, audio_file: Song) -> bool:
        """Нормализует громкость аудиофайла с проверкой"""
        if not self.validate_audio_file(audio_file):
            return False

        print(f"Normalizing audio: {audio_file.title}")
        return True

    def apply_fade_in(self, audio_file: Song, duration: float) -> bool:
        """Применяет fade-in эффект с проверкой параметров"""
        if not self.validate_audio_file(audio_file):
            return False

        if duration <= 0:
            raise ValueError("Fade-in duration must be positive")

        if duration > audio_file.duration:
            raise ValueError("Fade-in duration cannot exceed audio duration")

        print(f"Applying {duration}s fade-in to: {audio_file.title}")
        return True

    def apply_fade_out(self, audio_file: Song, duration: float) -> bool:
        """Применяет fade-out эффект с проверкой параметров"""
        if not self.validate_audio_file(audio_file):
            return False

        if duration <= 0:
            raise ValueError("Fade-out duration must be positive")

        if duration > audio_file.duration:
            raise ValueError("Fade-out duration cannot exceed audio duration")

        print(f"Applying {duration}s fade-out to: {audio_file.title}")
        return True

    def trim_audio(self, audio_file: Song, start: float, end: float) -> bool:
        """Обрезает аудиофайл с проверкой параметров"""
        if not self.validate_audio_file(audio_file):
            return False

        if start < 0:
            raise ValueError("Start time cannot be negative")

        if end <= start:
            raise ValueError("End time must be greater than start time")

        if end > audio_file.duration:
            raise ValueError("End time cannot exceed audio duration")

        print(f"Trimming {audio_file.title} from {start}s to {end}s")
        return True

    def merge_audio_files(self, files: List[Song]) -> Optional[Song]:
        """Объединяет несколько аудиофайлов в один с проверкой"""
        if not files:
            return None

        for file in files:
            if not self.validate_audio_file(file):
                raise AudioCorruptedException(f"Cannot merge invalid audio file: {file.file_path}")

        first_file = files[0]
        total_duration = sum(song.duration for song in files)

        merged_song = Song(
            f"merged_{first_file.file_path}",
            f"Merged: {first_file.title}",
            total_duration,
            "Various Artists",
            "Merged Album"
        )
        return merged_song

    def split_audio_file(self, audio_file: Song, segments: int) -> List[Song]:
        """Разделяет аудиофайл на сегменты с проверкой"""
        if not self.validate_audio_file(audio_file):
            return []

        if segments <= 0:
            raise ValueError("Number of segments must be positive")

        if segments > 100:
            raise ValueError("Too many segments requested")

        segment_duration = audio_file.duration / segments
        segments_list = []

        for i in range(segments):
            segment = Song(
                f"{audio_file.file_path}_part{i + 1}",
                f"{audio_file.title} Part {i + 1}",
                segment_duration,
                audio_file.artist,
                audio_file.album
            )
            segments_list.append(segment)

        return segments_list