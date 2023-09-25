from typing import Optional

from auth.model import AuthenticatedUser


users_mock = [
    {"id": "123", "email": "admin@mail.com", "role": "admin", "password": "123"},
    {"id": "321", "email": "e@mail.com", "role": "user", "password": "321"},
]


def get_user_auth(email: str, password: str) -> Optional[AuthenticatedUser]:
    filtered_users = [
        user for user in users_mock if user.get("email") == email and user.get("password") == password
    ]

    if filtered_users and len(filtered_users) > 0:
        return AuthenticatedUser(
            user_id=filtered_users[0]["id"],
            email=filtered_users[0]["email"],
            role=filtered_users[0]["role"],
            token="",
        )
    return None
