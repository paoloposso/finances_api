import unittest
from flask import Flask, jsonify
from unittest.mock import MagicMock, patch

from user.routes import create_user_blueprint


class AuthBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True

        self.auth_service_mock = MagicMock()

        self.app.register_blueprint(
            create_user_blueprint(self.auth_service_mock), url_prefix="/auth"
        )
        self.client = self.app.test_client()

    def test_login_success(self):
        self.auth_service_mock.login.return_value = "test_token"

        data = {"email": "test@example.com", "password": "password"}
        response = self.client.post("/auth/", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

        self.auth_service_mock.login.assert_called_with("test@example.com", "password")

    def test_login_missing_fields(self):
        data = {"email": "test@example.com"}  # Missing 'password'
        response = self.client.post("/auth/", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

        self.auth_service_mock.login.assert_not_called()


if __name__ == "__main__":
    unittest.main()
