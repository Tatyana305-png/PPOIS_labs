from datetime import datetime, timedelta
from .User import User
from Exceptions.SubscriptionExpiredException import SubscriptionExpiredException

class Subscription:
    def __init__(self, user: User):
        self.user = user
        self.plan_type = "free"
        self.start_date = datetime.now()
        self.end_date = datetime.now() + timedelta(days=30)
        self.is_active = True
        self.payment_method = ""
        self.auto_renew = True

    def check_validity(self):
        """Проверяет валидность подписки"""
        if datetime.now() > self.end_date:
            self.is_active = False
            raise SubscriptionExpiredException("Subscription has expired")
        return True