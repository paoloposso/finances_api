from typing import Optional

import bcrypt
import pymongo

from user.model import AuthenticatedUser, User
from user.repository import UserRepositoryABC


class UserRepository(UserRepositoryABC):
    def __init__(self, db_client: pymongo.MongoClient, db_name: str):
        self.users_collection_name = "users"
        self.db_client = db_client
        self.db_name = db_name

        client_collection = self.db_client[db_name].get_collection("clients")
        client_collection.create_index([("email", pymongo.ASCENDING)], unique=True)

    def create_user(self, user: User, plain_password: str) -> str:
        hashed_password = self._hash_password(plain_password)
        user_collection = self.db_client[self.db_name][self.users_collection_name]
        result = user_collection.insert_one(
            {"email": user.email, "password": hashed_password, "role": user.role}
        )

        return str(result.inserted_id)

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

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
