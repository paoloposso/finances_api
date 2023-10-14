import unittest
from flask import Flask
from unittest.mock import MagicMock, patch

from user.service import UserService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True

        self.repository_mock = MagicMock()
        self.service = UserService(self.repository_mock)

        self.client = self.app.test_client()

    def test_create_user(self):
        self.repository_mock.create_user.return_value = "test_id"
        self.repository_mock.get_user_by_email.return_value = None

        inserted_id = self.service.create_user("email@test.com", "1234", "admin")

        self.assertEqual(inserted_id, "test_id")

        self.repository_mock.create_user.assert_called_with(
            "email@test.com", "1234", "admin"
        )


if __name__ == "__main__":
    unittest.main()
