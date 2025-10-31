class SoftwareException(Exception):
    """Базовое исключение для программных ошибок"""
    pass

class ApplicationCrashException(SoftwareException):
    """Исключение краха приложения"""
    pass

class DependencyMissingException(SoftwareException):
    """Исключение отсутствия зависимости"""
    pass

class VersionCompatibilityException(SoftwareException):
    """Исключение несовместимости версий"""
    pass