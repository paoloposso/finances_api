from flask import Blueprint

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    return "Hello, World transactions!"
