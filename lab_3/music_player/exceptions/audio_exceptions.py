class AudioException(Exception):
    """Базовое исключение для аудио"""
    pass

class InvalidAudioFormatException(AudioException):
    """Неподдерживаемый формат аудио"""
    pass

class AudioFileNotFoundException(AudioException):
    """Аудио файл не найден"""
    pass

class AudioCorruptedException(AudioException):
    """Аудио файл поврежден"""
    pass

class AudioPermissionException(AudioException):
    """Нет прав доступа к аудио файлу"""
    pass