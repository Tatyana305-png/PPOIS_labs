import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.UserBehaviors.UserManager import UserManager
from Behaviors.UserBehaviors.SubscriptionManager import SubscriptionManager
from Behaviors.UserBehaviors.UserAnalytics import UserAnalytics
from Behaviors.UserBehaviors.SocialFeatures import SocialFeatures
from Models.UserModels.User import User


class TestUserBehaviors(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()
        self.subscription_manager = SubscriptionManager()
        self.user_analytics = UserAnalytics()
        self.social_features = SocialFeatures()

        # Создаем тестовых пользователей
        self.user1 = User("user1", "john_doe", "john@example.com")
        self.user2 = User("user2", "jane_smith", "jane@example.com")

    def test_register_user(self):
        """Тест регистрации нового пользователя"""
        new_user = self.user_manager.register_user("newuser", "new@example.com", "password123")

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, "newuser")
        self.assertEqual(new_user.email, "new@example.com")
        self.assertTrue(new_user.is_active)
        self.assertIsNotNone(new_user.user_id)

    def test_authenticate_user_success(self):
        """Тест успешной аутентификации пользователя"""
        user = self.user_manager.authenticate_user("john_doe", "password")

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "john_doe")
        self.assertIn("john_doe", user.email)

    def test_authenticate_user_none(self):
        """Тест аутентификации с неверными данными"""
        user = self.user_manager.authenticate_user("nonexistent", "wrongpass")
        self.assertIsNotNone(user)

    def test_update_user_profile(self):
        """Тест обновления профиля пользователя"""
        profile_data = {
            "first_name": "John",
            "last_name": "Doe",
            "country": "USA",
            "bio": "Music lover"
        }

        result = self.user_manager.update_user_profile(self.user1, profile_data)
        self.assertTrue(result)

    def test_change_password(self):
        """Тест смены пароля"""
        result = self.user_manager.change_password(self.user1, "oldpass", "newpass")
        self.assertTrue(result)

    def test_delete_user_account(self):
        """Тест удаления аккаунта пользователя"""
        result = self.user_manager.delete_user_account(self.user1)
        self.assertTrue(result)

    def test_search_users(self):
        """Тест поиска пользователей"""
        users = self.user_manager.search_users("john")
        self.assertIsInstance(users, list)

    def test_follow_and_unfollow_user(self):
        """Тест подписки и отписки от пользователя"""
        # Подписка
        follow_result = self.user_manager.follow_user(self.user1, self.user2)
        self.assertTrue(follow_result)

        # Отписка
        unfollow_result = self.user_manager.unfollow_user(self.user1, self.user2)
        self.assertTrue(unfollow_result)

    def test_get_followers_and_following(self):
        """Тест получения подписчиков и подписок"""
        followers = self.user_manager.get_followers(self.user1)
        following = self.user_manager.get_following(self.user1)

        self.assertIsInstance(followers, list)
        self.assertIsInstance(following, list)

if __name__ == '__main__':
    unittest.main()