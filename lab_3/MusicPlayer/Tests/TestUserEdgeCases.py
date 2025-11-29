import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.UserManager import UserManager
from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager
from Models.UserModels.User import User


class TestUserEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для пользователей"""

    def setUp(self):
        self.user_manager = UserManager()
        self.subscription_manager = SubscriptionManager()

    def test_empty_search_query(self):
        """Тест поиска с пустым запросом"""
        users = self.user_manager.search_users("")
        self.assertIsInstance(users, list)

    def test_nonexistent_user_operations(self):
        """Тест операций с несуществующим пользователем"""
        nonexistent_user = User("nonexistent", "ghost", "ghost@example.com")

        result1 = self.user_manager.update_user_profile(nonexistent_user, {})
        result2 = self.user_manager.delete_user_account(nonexistent_user)

        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_subscription_with_none_user(self):
        """Тест создания подписки с None пользователем"""
        # Ожидаем ошибку, так как это правильное поведение
        with self.assertRaises(ValueError) as context:
            self.subscription_manager.create_subscription(None, "free")

        self.assertEqual(str(context.exception), "User is required")


if __name__ == '__main__':
    unittest.main()