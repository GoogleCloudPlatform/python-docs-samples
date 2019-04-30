# Copyright Google Inc.
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

"""
Sample application that demonstrates refreshing a session when using
Identity Aware Proxy. This application is for App Engine Standard.
"""

import flask
from google.appengine.api import users

app = flask.Flask(__name__)


@app.route('/')
def index():
    user = users.get_current_user()
    if user:
        logged_in = True
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        login_url = None
    else:
        logged_in = False
        nickname = None
        logout_url = None
        login_url = users.create_login_url('/')

    template_values = {
        'logged_in': logged_in,
        'nickname': nickname,
        'logout_url': logout_url,
        'login_url': login_url,
    }

    return flask.render_template('index.html', **template_values)


# Fake status
@app.route('/status')
def status():
    return 'Success'
