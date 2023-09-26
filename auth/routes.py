from flask import Blueprint, jsonify, request
from auth.repository import UserRepository

from auth.service import AuthService


def create_auth_blueprint(db_client, db_name):
    auth_bp = Blueprint("auth", __name__)
    auth_service = AuthService(user_repository=UserRepository(db_client, db_name))

    @auth_bp.route("/", methods=["POST"])
    def login():
        try:
            data = request.get_json()

            # Check if the 'email' and 'password' keys are in the request data
            if "email" not in data or "password" not in data:
                return jsonify({"error": "Missing email or password"}), 400

            # Extract the email and password
            email = data["email"]
            password = data["password"]

            token = auth_service.login(email, password)

            if token and token != "":
                return jsonify({"token": token}), 200
            else:
                return jsonify({"error": "Login failed"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return auth_bp
