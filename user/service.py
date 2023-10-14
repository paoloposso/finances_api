from abc import ABC, abstractmethod
from typing import Optional

import bcrypt
from user.exceptions import InvalidDataException, UserAlreadyExistsException
from user.model import User
from user.repository import UserRepositoryABC

from user.tokenization import generate_token


class UserServiceABC(ABC):
    @abstractmethod
    def login(self, email, password) -> Optional[str]:
        pass

    @abstractmethod
    def create_user(self, user: User, plain_password: str) -> str:
        pass


class UserService(UserServiceABC):
    def __init__(self, user_repository: UserRepositoryABC):
        self.user_repository = user_repository

    def login(self, email, hashed_password) -> Optional[str]:
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            return None

        if bcrypt.checkpw(hashed_password.encode("utf-8"), user.password):
            return generate_token(user.user_id, user.role)

        return None

    def create_user(self, user: User, plain_password: str) -> str:
        if user.email is None or len(user.email) == 0:
            raise InvalidDataException("User e-mail cannot be empty")
        if plain_password is None or len(plain_password) == 0:
            raise InvalidDataException("User password cannot be empty")
        if user.role is None or len(user.role) == 0:
            raise InvalidDataException("User role cannot be empty")
        if user.name is None or len(user.name) == 0:
            raise InvalidDataException("User name cannot be empty")

        existing_user = self.user_repository.get_user_by_email(user.email)
        if existing_user is not None:
            raise UserAlreadyExistsException(f"User e-mail {user.email} already exists")

        return self.user_repository.create_user(user, plain_password)

    def _get_user_by_email_and_password(
        self, email: str, password: str
    ) -> Optional[dict]:
        user_collection = self.db_client[self.db_name][self.users_collection_name]
        user_document = user_collection.find_one({"email": email})

        if user_document and bcrypt.checkpw(
            password.encode("utf-8"), user_document["password"]
        ):
            return {
                "id": user_document.get("_id", ""),
                "email": user_document.get("email", ""),
                "role": user_document.get("role", ""),
            }

        return None
