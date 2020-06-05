import os
import json

from flask import Flask

app = Flask(__name__)
cache = {'get_count': 0, 'post_count': 0}

@app.route('/', methods=['GET'])
def hello_world():
    cache['get_count'] += 1
    return json.dumps(cache)

@app.route('/', methods=['POST'])
def event_handler():
    cache['post_count'] += 1
    return json.dumps(cache)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
