from flask import Flask, request
import os

app = Flask(__name__)


@app.route("/flag", methods=["GET", "POST"])
def flag():
    username = request.form.get("username")
    password = request.headers.get("password")
    if username and username == "admin" and password and password == "admin":
        return os.getenv('FLAG')
    return "So close"


@app.get('/test')
def test():
    return "test"


app.run(host='0.0.0.0', port=5000)
