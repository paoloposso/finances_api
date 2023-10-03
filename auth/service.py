from abc import ABC, abstractmethod
from typing import Optional
from auth.repository import UserRepository

from auth.tokenization import generate_token


class AuthServiceABC(ABC):
    @abstractmethod
    def login(self, email, password) -> Optional[str]:
        pass


class AuthService(AuthServiceABC):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, email, password) -> Optional[str]:
        user = self.user_repository.get_user_auth(email, password)
        if user is None:
            return None
        user_id = user.user_id
        access_token = generate_token(user_id, user.role)

        return access_token
