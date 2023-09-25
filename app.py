from flask import Flask
from auth.routes import auth_bp
from transactions.routes import transactions_bp

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(transactions_bp, url_prefix='/transactions')

if __name__ == '__main__':
    app.run(debug=True)
