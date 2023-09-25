from typing import Optional

from auth.model import UserAuth


def get_user_auth(email: str, password: str) -> Optional[UserAuth]:
    if email == "test" and password == "test":
        return UserAuth("123", "test", "admin")
    return None
