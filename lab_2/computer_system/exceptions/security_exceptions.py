class SecurityException(Exception):
    """Базовое исключение для ошибок безопасности"""
    pass

class AuthenticationException(SecurityException):
    """Исключение аутентификации"""
    pass

class EncryptionException(SecurityException):
    """Исключение шифрования"""
    pass

class PermissionDeniedException(SecurityException):
    """Исключение отказа в доступе"""
    pass

class SecurityBreachException(SecurityException):
    """Исключение нарушения безопасности"""
    pass