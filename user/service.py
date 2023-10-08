from abc import ABC, abstractmethod
from typing import Optional
from user.exceptions import InvalidDataException, UserAlreadyExistsException
from user.repository import UserRepositoryABC

from user.tokenization import generate_token


class UserServiceABC(ABC):
    @abstractmethod
    def login(self, email, password) -> Optional[str]:
        pass

    @abstractmethod
    def create_user(self, email, password):
        pass


class UserService(UserServiceABC):
    def __init__(self, user_repository: UserRepositoryABC):
        self.user_repository = user_repository

    def login(self, email, password) -> Optional[str]:
        user = self.user_repository.get_user_auth(email, password)
        if user is None:
            return None
        user_id = user.user_id
        access_token = generate_token(user_id, user.role)

        return access_token

    def create_user(self, email, password, role) -> str:
        if email is None or len(email) == 0:
            raise InvalidDataException("User e-mail cannot be empty")
        if password is None or len(password) == 0:
            raise InvalidDataException("User password cannot be empty")
        if role is None or len(role) == 0:
            raise InvalidDataException("User role cannot be empty")

        if self.user_repository.get_user_by_email(email) is not None:
            raise UserAlreadyExistsException(f"User e-mail {email} already exists")

        return self.user_repository.create_user(email, password, role)
