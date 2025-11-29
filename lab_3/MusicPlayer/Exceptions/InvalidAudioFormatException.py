from .AudioException import AudioException

class InvalidAudioFormatException(AudioException):
    """Неподдерживаемый формат аудио"""
    pass