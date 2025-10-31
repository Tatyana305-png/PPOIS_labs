class UserException(Exception):
    """Базовое исключение для пользователей"""
    pass

class UserNotFoundException(UserException):
    """Пользователь не найден"""
    pass

class InsufficientPermissionsException(UserException):
    """Недостаточно прав"""
    pass

class SubscriptionExpiredException(UserException):
    """Подписка истекла"""
    pass