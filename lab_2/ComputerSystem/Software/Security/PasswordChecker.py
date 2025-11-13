class PasswordChecker:
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special = True

    def is_strong_password(self, password: str) -> bool:
        """Проверка сложности пароля"""
        if len(password) < self.min_length:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if self.require_uppercase and not has_upper:
            return False
        if self.require_lowercase and not has_lower:
            return False
        if self.require_numbers and not has_digit:
            return False
        if self.require_special and not has_special:
            return False

        return True