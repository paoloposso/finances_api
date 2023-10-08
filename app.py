import os
from flask import Flask
from flask.cli import load_dotenv
from flask_jwt_extended import JWTManager
import pymongo
from user.infrastructure.user_mongo import UserRepository
from user.routes import create_user_blueprint
from user.service import UserService
from transactions.routes import transactions_bp

app = Flask(__name__)

load_dotenv()

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "")

jwt = JWTManager(app)


def initialize_database() -> dict:
    os.environ.get("MONGO_URL", "")

    mongo_url = os.environ.get("MONGO_URL", "")  # "mongodb://localhost:27017"
    database_name = os.environ.get("MONGO_DATABASE_NAME", "")

    client = pymongo.MongoClient(mongo_url)

    return {"client": client, "db_name": database_name}


def initialize_routes(client: pymongo.MongoClient, db_name: str):
    app.register_blueprint(
        create_user_blueprint(UserService(UserRepository(client, db_name))),
        url_prefix="/auth",
    )
    app.register_blueprint(transactions_bp, url_prefix="/transactions")


@app.route("/")
def index():
    return "API is running!"


db_dict = initialize_database()
initialize_routes(db_dict["client"], db_dict["db_name"])

if __name__ == "__main__":
    app.run(debug=True)
