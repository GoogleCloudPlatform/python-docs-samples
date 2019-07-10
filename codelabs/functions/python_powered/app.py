from main import python_powered
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return python_powered(request)
