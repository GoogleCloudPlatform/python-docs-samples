import sys
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def say_hello():
    return 'Flask server 1 says hello!'

@app.route('/')
def root():
    return 'This is flask server 1.'

if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--development':
        app.run(port=int(8001))
    else:
        app.run()
