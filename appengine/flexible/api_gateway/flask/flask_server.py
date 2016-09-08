import sys
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def say_hello():
    return 'The Flask server says hello!'

@app.route('/')
def root():
    return 'This is a flask server.'

if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'development':
        app.run(port=int(8001))
    else:
        app.run()
