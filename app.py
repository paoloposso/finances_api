import os
from flask import Flask
from flask_jwt_extended import JWTManager
from auth.routes import auth_bp
from transactions.routes import transactions_bp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "")

jwt = JWTManager(app)


@app.route("/")
def index():
    return "API is running!"


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(transactions_bp, url_prefix="/transactions")

if __name__ == "__main__":
    app.run(debug=True)
