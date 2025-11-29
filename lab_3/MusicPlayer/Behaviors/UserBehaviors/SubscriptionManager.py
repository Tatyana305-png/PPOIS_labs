from Models.UserModels.User import User
from Models.UserModels.Subscription import Subscription

class SubscriptionManager:
    """Управление подписками пользователей"""

    def create_subscription(self, user: User, plan_type: str) -> Subscription:
        """Создает новую подписку для пользователя"""
        if not user:
            raise ValueError("User is required")

        valid_plans = ["free", "premium", "family"]
        if plan_type not in valid_plans:
            raise ValueError(f"Invalid plan type. Must be one of: {valid_plans}")

        subscription = Subscription(user)
        subscription.plan_type = plan_type
        return subscription

    def upgrade_subscription(self, subscription: Subscription, new_plan: str) -> bool:
        """Улучшает подписку"""
        return self.change_plan(subscription, new_plan)

    def change_plan(self, subscription: Subscription, new_plan: str) -> bool:
        """Изменяет тарифный план подписки"""
        if not subscription or not subscription.is_active:
            return False

        valid_plans = ["free", "premium", "family"]
        if new_plan not in valid_plans:
            return False

        subscription.plan_type = new_plan
        return True

    def cancel_subscription(self, subscription: Subscription) -> bool:
        """Отменяет подписку"""
        if not subscription:
            return False

        subscription.is_active = False
        return True

    def check_subscription_status(self, subscription: Subscription) -> bool:
        """Проверяет статус подписки"""
        return self.is_subscription_active(subscription)

    def is_subscription_active(self, subscription: Subscription) -> bool:
        """Проверяет активна ли подписка"""
        return bool(subscription and subscription.is_active)

    def process_payment(self, subscription: Subscription, amount: float) -> bool:
        """Обрабатывает платеж"""
        return True

    def get_billing_history(self, user: User) -> list:
        """Возвращает историю платежей"""
        return []