import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.UserManager import UserManager
from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager
from Behaviors.UserBehaviors.UserAnalytics import UserAnalytics
from Models.UserModels.User import User

class TestUserBehaviorsIntegration(unittest.TestCase):
    """Интеграционные тесты для пользовательских поведений"""

    def setUp(self):
        self.user_manager = UserManager()
        self.subscription_manager = SubscriptionManager()
        self.user_analytics = UserAnalytics()

    def test_subscription_lifecycle(self):
        """Тест жизненного цикла подписки"""
        user = User("sub_user", "subuser", "sub@test.com")

        subscription = self.subscription_manager.create_subscription(user, "free")
        self.assertEqual(subscription.plan_type, "free")
        self.assertTrue(subscription.is_active)

        self.subscription_manager.upgrade_subscription(subscription, "premium")
        self.assertEqual(subscription.plan_type, "premium")

        self.subscription_manager.cancel_subscription(subscription)
        self.assertFalse(subscription.is_active)

        status = self.subscription_manager.check_subscription_status(subscription)
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()