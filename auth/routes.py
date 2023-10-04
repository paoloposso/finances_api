from flask import Blueprint, jsonify, request
from auth.exceptions import InvalidDataException, UserAlreadyExistsException
from auth.repository import UserRepository

from auth.service import AuthService


def create_auth_blueprint(db_client, db_name):
    auth_bp = Blueprint("auth", __name__)
    auth_service = AuthService(user_repository=UserRepository(db_client, db_name))

    @auth_bp.route("/", methods=["POST"])
    def login():
        try:
            data = request.get_json()

            if "email" not in data or "password" not in data:
                return jsonify({"error": "Missing email or password"}), 400

            email = data.get("email", "")
            password = data.get("password", "")

            token = auth_service.login(email, password)

            if token and token != "":
                return jsonify({"token": token}), 200
            else:
                return jsonify({"error": "Login failed"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @auth_bp.route("/create", methods=["POST"])
    def create_user():
        try:
            data = request.get_json()

            if "email" not in data or "password" not in data:
                return jsonify({"error": "Missing email or password"}), 400

            email = data.get("email", "")
            password = data.get("password", "")
            role = data.get("role", "")

            return (
                jsonify({"user_id": auth_service.create_user(email, password, role)}),
                200,
            )
        except UserAlreadyExistsException as e:
            return jsonify({"error": str(e)}), 400
        except InvalidDataException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return auth_bp
