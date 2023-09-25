from flask_jwt_extended import create_access_token, decode_token
from jwt import InvalidTokenError


def generate_token(user_id: str, role: str) -> str:
    access_token = create_access_token(identity=user_id, additional_claims={'role': role})
    return access_token


def get_user_id_from_token(token: str) -> str:
    """Extracts user id from token"""
    try:
        payload = decode_token(token)
        user_id = payload['identity']
        return user_id
    except Exception as e:
        raise InvalidTokenError(e)