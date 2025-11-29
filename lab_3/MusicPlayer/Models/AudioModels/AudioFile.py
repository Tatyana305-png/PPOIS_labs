from datetime import datetime
from Exceptions.InvalidAudioFormatException import InvalidAudioFormatException

class AudioFile:
    def __init__(self, file_path: str, title: str, duration: float):
        self.file_path = file_path
        self.title = title
        self.duration = duration
        self.file_size = 0
        self.bitrate = 320
        self.sample_rate = 44100
        self.channels = 2
        self.format = "mp3"
        self.creation_date = datetime.now()
        self.modification_date = datetime.now()

    def validate_format(self):
        if self.format not in ["mp3", "wav", "flac", "aac"]:
            raise InvalidAudioFormatException(f"Unsupported format: {self.format}")