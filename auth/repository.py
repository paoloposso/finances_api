from abc import ABC, abstractmethod
from typing import Optional
import bcrypt

import pymongo

from auth.model import AuthenticatedUser
from auth.tokenization import generate_token


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


class UserRepository:
    def __init__(self, db_client: pymongo.MongoClient, db_name: str):
        self.users_collection_name = "users"
        self.db_client = db_client
        self.db_name = db_name

        client_collection = self.db_client[db_name].get_collection("clients")
        client_collection.create_index([("email", pymongo.ASCENDING)], unique=True)

    def create_user(self, email: str, password: str, role: str) -> str:
        hashed_password = self._hash_password(password)
        user_collection = self.db_client[self.db_name][self.users_collection_name]
        result = user_collection.insert_one(
            {"email": email, "password": hashed_password, "role": role}
        )

        return str(result.inserted_id)

    def get_user_auth(self, email: str, password: str) -> Optional[AuthenticatedUser]:
        user = self._get_user_by_email_and_password(email, password)

        if user is not None and len(user) > 0:
            user_id = str(user.get("id", ""))
            result = AuthenticatedUser(
                user_id=user_id,
                email=user.get("email", ""),
                role=user.get("role", ""),
                token=generate_token(
                    user_id,
                    user.get("role", ""),
                ),
            )
            return result
        return None

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        user_collection = self.db_client[self.db_name][self.users_collection_name]
        user_document = user_collection.find_one({"email": email})

        if user_document:
            return {
                "id": user_document.get("_id", ""),
                "email": user_document.get("email", ""),
                "role": user_document.get("role", ""),
            }

        return None

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

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
