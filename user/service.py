from abc import ABC, abstractmethod
from typing import Optional

import bcrypt
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
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            return None

        if bcrypt.checkpw(password.encode("utf-8"), user.password):
            return generate_token(user.user_id, user.role)

        return None

    def create_user(self, email: str, password: str, role: str) -> str:
        if email is None or len(email) == 0:
            raise InvalidDataException("User e-mail cannot be empty")
        if password is None or len(password) == 0:
            raise InvalidDataException("User password cannot be empty")
        if role is None or len(role) == 0:
            raise InvalidDataException("User role cannot be empty")

        if self.user_repository.get_user_by_email(email) is not None:
            raise UserAlreadyExistsException(f"User e-mail {email} already exists")

        return self.user_repository.create_user(email, password, role)

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
