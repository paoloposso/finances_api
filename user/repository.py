from abc import ABC, abstractmethod
from typing import Optional

from user.model import AuthenticatedUser


class UserRepositoryABC(ABC):
    @abstractmethod
    def get_user_auth(self, email: str, password: str) -> Optional[AuthenticatedUser]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        pass

    @abstractmethod
    def create_user(self, email: str, password: str, role: str) -> str:
        pass
