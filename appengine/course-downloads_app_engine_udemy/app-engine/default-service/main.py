from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'My Default Service - V1'