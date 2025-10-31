class PlaylistException(Exception):
    """Базовое исключение для плейлистов"""
    pass

class PlaylistNotFoundException(PlaylistException):
    """Плейлист не найден"""
    pass

class PlaylistEmptyException(PlaylistException):
    """Плейлист пуст"""
    pass

class DuplicateSongException(PlaylistException):
    """Дублирование песни в плейлисте"""
    pass