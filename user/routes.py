from flask import Blueprint, jsonify, request
from user.exceptions import InvalidDataException, UserAlreadyExistsException
from user.model import User

from user.service import UserServiceABC


def create_user_blueprint(auth_service: UserServiceABC):
    auth_bp = Blueprint("auth", __name__)

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

            if (
                "email" not in data
                or "password" not in data
                or "role" not in data
                or "name" not in data
            ):
                return jsonify({"error": "Missing required fields"}), 400

            email = data.get("email", "")
            plain_password = data.get("password", "")
            role = data.get("role", "")
            name = data.get("name", "")

            return (
                jsonify(
                    {
                        "user_id": auth_service.create_user(
                            User(email, role, name), plain_password
                        )
                    }
                ),
                200,
            )
        except UserAlreadyExistsException as e:
            return jsonify({"error": str(e)}), 400
        except InvalidDataException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return auth_bp
