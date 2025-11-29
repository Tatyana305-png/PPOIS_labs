import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager
from Models.UserModels.User import User

class TestSubscriptionManager(unittest.TestCase):

    def setUp(self):
        self.subscription_manager = SubscriptionManager()
        self.user = User("user1", "testuser", "test@example.com")


    def test_upgrade_subscription(self):
        """Тест улучшения подписки"""
        subscription = self.subscription_manager.create_subscription(self.user, "free")
        result = self.subscription_manager.upgrade_subscription(subscription, "premium")

        self.assertTrue(result)
        self.assertEqual(subscription.plan_type, "premium")

    def test_cancel_subscription(self):
        """Тест отмены подписки"""
        subscription = self.subscription_manager.create_subscription(self.user, "premium")
        result = self.subscription_manager.cancel_subscription(subscription)

        self.assertTrue(result)
        self.assertFalse(subscription.is_active)

    def test_check_subscription_status(self):
        """Тест проверки статуса подписки"""
        subscription = self.subscription_manager.create_subscription(self.user, "premium")
        status = self.subscription_manager.check_subscription_status(subscription)

        self.assertTrue(status)

        # Отменяем и проверяем снова
        self.subscription_manager.cancel_subscription(subscription)
        status_after_cancel = self.subscription_manager.check_subscription_status(subscription)
        self.assertFalse(status_after_cancel)

    def test_process_payment(self):
        """Тест обработки платежа"""
        subscription = self.subscription_manager.create_subscription(self.user, "premium")
        result = self.subscription_manager.process_payment(subscription, 9.99)

        self.assertTrue(result)

    def test_get_billing_history(self):
        """Тест получения истории платежей"""
        billing_history = self.subscription_manager.get_billing_history(self.user)

        self.assertIsInstance(billing_history, list)

if __name__ == '__main__':
    unittest.main()