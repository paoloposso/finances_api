from abc import ABC, abstractmethod
from typing import Optional

from user.model import AuthenticatedUser, User


class UserRepositoryABC(ABC):
    @abstractmethod
    def get_user_auth(self, email: str, password: str) -> Optional[AuthenticatedUser]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        pass

    @abstractmethod
    def create_user(self, user: User, plain_password: str) -> str:
        pass
