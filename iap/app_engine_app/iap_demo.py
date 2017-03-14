# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demo App Engine standard environment app for Identity-Aware Proxy.

The / handler returns the contents of the JWT header, for use in
iap_test.py.

The /identity handler demonstrates how to use the Google App Engine
standard environment's Users API to obtain the identity of users
authenticated by Identity-Aware Proxy.

To deploy this app, follow the instructions in
https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_third-party_library
to install the flask library into your application.
"""
import flask

from google.appengine.api import users


app = flask.Flask(__name__)


@app.route('/')
def echo_jwt():
    return 'x-goog-authenticated-user-jwt: {}'.format(
        flask.request.headers.get('x-goog-authenticated-user-jwt'))


@app.route('/identity')
def show_identity():
    user = users.get_current_user()
    return 'Authenticated as {} ({})'.format(
        user.email(), user.user_id())
