from typing import Optional

import pymongo

from auth.model import AuthenticatedUser
from auth.tokenization import generate_token


users_mock = [
    {"id": "123", "email": "admin@mail.com", "role": "admin", "password": "123"},
    {"id": "321", "email": "e@mail.com", "role": "user", "password": "321"},
]


class UserRepository:
    def __init__(self, db_client: pymongo.MongoClient, db_name: str):
        self.users_collection_name = "users"
        self.db_client = db_client
        self.db_name = db_name

        client_collection = self.db_client[db_name].get_collection("clients")
        client_collection.create_index(
            [("email", pymongo.ASCENDING), ("password", pymongo.ASCENDING)]
        )

    def get_user_auth(self, email: str, password: str) -> Optional[AuthenticatedUser]:
        filtered_users = self._get_user_by_email_and_password(email, password)

        if filtered_users is not None and len(filtered_users) > 0:
            return AuthenticatedUser(
                user_id=filtered_users[0]["id"],
                email=filtered_users[0]["email"],
                role=filtered_users[0]["role"],
                token=generate_token(
                    filtered_users[0]["id"], filtered_users[0]["role"]
                ),
            )
        return None

    def _get_user_by_email_and_password(
        self, email: str, password: str
    ) -> Optional[dict]:
        user_collection = self.db_client[self.db_name][self.users_collection_name]
        user_document = user_collection.find_one({"email": email, "password": password})

        if user_document:
            return {
                "id": user_document["_id"],
                "email": user_document["email"],
                "role": user_document["role"],
            }
        return None
