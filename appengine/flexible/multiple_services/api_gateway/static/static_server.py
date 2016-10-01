import sys
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def say_hello():
    return 'Flask server 2 says hello!'

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    mimetype = ''
    if path.split('.')[1] == 'css':
        mimetype = 'text/css'
    if path.split('.')[1] == 'js':
        mimetype = 'application/javascript'
    return app.send_static_file(path), 200, {'Content-Type': mimetype}

if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'development':
        app.run(port=int(8003))
    else:
        app.run()
