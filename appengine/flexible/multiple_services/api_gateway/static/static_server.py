import os
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def say_hello():
    '''responds to request from frontend via gateway'''
    return 'Static File Server says hello!'

@app.route('/')
def root():
    '''serves index.html'''
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    '''serves static files required by index.html'''
    mimetype = ''
    if path.split('.')[1] == 'css':
        mimetype = 'text/css'
    if path.split('.')[1] == 'js':
        mimetype = 'application/javascript'
    return app.send_static_file(path), 200, {'Content-Type': mimetype}

if __name__  == "__main__":
    port = os.environ.get('PORT') or 8001
    app.run(port=port)
