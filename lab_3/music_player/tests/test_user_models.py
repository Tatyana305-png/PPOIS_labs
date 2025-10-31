import unittest
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_models import User, UserProfile, Subscription, ListeningHistory
from exceptions.user_exceptions import SubscriptionExpiredException


class TestUserModels(unittest.TestCase):

    def setUp(self):
        self.user = User("user123", "testuser", "test@example.com")
        self.profile = UserProfile(self.user)
        self.subscription = Subscription(self.user)
        self.history = ListeningHistory(self.user)

    def test_user_creation(self):
        self.assertEqual(self.user.user_id, "user123")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)

    def test_user_profile_association(self):
        self.assertEqual(self.profile.user, self.user)
        self.profile.first_name = "John"
        self.profile.last_name = "Doe"
        self.assertEqual(self.profile.first_name, "John")
        self.assertEqual(self.profile.last_name, "Doe")

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan_type, "free")
        self.assertTrue(self.subscription.is_active)

    def test_subscription_validity_valid(self):
        self.subscription.end_date = datetime.now() + timedelta(days=30)
        try:
            self.subscription.check_validity()
            self.assertTrue(True)
        except SubscriptionExpiredException:
            self.fail("Valid subscription raised exception")

    def test_subscription_validity_expired(self):
        self.subscription.end_date = datetime(2020, 1, 1)
        with self.assertRaises(SubscriptionExpiredException):
            self.subscription.check_validity()

    def test_listening_history_association(self):
        self.assertEqual(self.history.user, self.user)
        self.assertEqual(self.history.entries, [])
        self.assertEqual(self.history.total_listening_time, 0)

    def test_user_preferences_defaults(self):
        self.user.preferences = {"theme": "dark", "language": "en"}
        self.assertEqual(self.user.preferences["theme"], "dark")
        self.assertEqual(self.user.preferences["language"], "en")


if __name__ == '__main__':
    unittest.main()