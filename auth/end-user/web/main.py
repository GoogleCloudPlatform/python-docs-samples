# Copyright 2017 Google Inc. All Rights Reserved.
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

"""An example web application that obtains authorization and credentials from
an end user.

This sample is used on
https://developers.google.com/identity/protocols/OAuth2WebServer. Please
refer to that page for instructions on using this sample.

Notably, you'll need to obtain a OAuth2.0 client secrets file and set the
``GOOGLE_CLIENT_SECRETS`` environment variable to point to that file.
"""

import os

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# The path to the client-secrets.json file obtained from the Google API
# Console. You must set this before running this application.
CLIENT_SECRETS_FILENAME = os.environ['GOOGLE_CLIENT_SECRETS']
# The OAuth 2.0 scopes that this application will ask the user for. In this
# case the application will ask for basic profile information.
SCOPES = ['email', 'profile']

app = flask.Flask(__name__)
# TODO: A secret key is included in the sample so that it works but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'TODO: replace with a secret value'


@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # Get the basic user info from the Google OAuth2.0 API.
    client = googleapiclient.discovery.build(
        'oauth2', 'v2', credentials=credentials)

    response = client.userinfo().v2().me().get().execute()

    return str(response)


@app.route('/authorize')
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # an access token and a refresh token for the user's credentials.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true')

    # Store the state in the session so that the callback can verify the
    # authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    credentials = flow.credentials
    flask.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    # When running locally with Flask's development server this disables
    # OAuthlib's HTTPs verification. When running in production with a WSGI
    # server such as gunicorn this option will not be set and your application
    # *must* use HTTPS.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)
