# Copyright 2016 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask

app = Flask(__name__)


@app.route('/hello')
def say_hello():
    """responds to request from frontend via gateway"""
    return 'Static File Server says hello!'


@app.route('/')
def root():
    """serves index.html"""
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_file(path):
    """serves static files required by index.html"""
    mimetype = ''
    if '.' in path and path.split('.')[1] == 'css':
        mimetype = 'text/css'
    if '.' in path and path.split('.')[1] == 'js':
        mimetype = 'application/javascript'
    return app.send_static_file(path), 200, {'Content-Type': mimetype}


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8001, debug=True)
