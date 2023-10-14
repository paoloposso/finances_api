import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from user.exceptions import InvalidDataException, UserAlreadyExistsException
from user.model import User

from user.service import UserService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True

        self.repository_mock = MagicMock()
        self.service = UserService(self.repository_mock)

        self.client = self.app.test_client()

    def test_create_user(self):
        # Create a MagicMock for the User class
        user_mock = MagicMock()
        user_mock.email = "email@test.com"
        user_mock.role = "admin"
        user_mock.name = "paolo"

        self.repository_mock.create_user.return_value = "test_id"
        self.repository_mock.get_user_by_email.return_value = None

        inserted_id = self.service.create_user(user_mock, "1234")

        self.assertEqual(inserted_id, "test_id")

        # Check if create_user was called with the User object and "1234"
        self.repository_mock.create_user.assert_called_with(user_mock, "1234")


    def test_create_user_fail_existing_user(self):
        self.repository_mock.create_user.return_value = "test_id"

        with self.assertRaises(UserAlreadyExistsException) as context:
            self.service.create_user(User("email@test.com", "admin", "paolo"), "1234")

    def test_create_user_fail_missing_data(self):
        self.repository_mock.create_user.return_value = "test_id"

        with self.assertRaises(InvalidDataException) as context:
            self.service.create_user(User("email@test.com", "", "paolo"), "1234")


if __name__ == "__main__":
    unittest.main()
