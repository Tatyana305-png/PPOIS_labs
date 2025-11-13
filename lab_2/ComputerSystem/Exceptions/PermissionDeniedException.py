from .SecurityException import SecurityException

class PermissionDeniedException(SecurityException):
    """Исключение отказа в доступе"""
    pass