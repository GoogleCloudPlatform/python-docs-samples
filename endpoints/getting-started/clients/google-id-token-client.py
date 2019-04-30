#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Example of calling a Google Cloud Endpoint API with an ID token obtained
using the Google OAuth2 flow."""

import argparse

import google_auth_oauthlib.flow
import requests
from six.moves import urllib


def get_id_token(client_secrets_file, extra_args):
    """Obtains credentials from the user using OAuth 2.0 and then returns the
    ID token from those credentials."""

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes=['openid', 'email', 'profile'])

    # Run the OAuth 2.0 flow to obtain credentials from the user.
    flow.run_local_server()

    # The credentials have both an access token and an ID token. Cloud
    # Endpoints uses the ID Token.
    id_token = flow.oauth2session.token['id_token']

    return id_token


def make_request(host, api_key, id_token):
    """Makes a request to the auth info endpoint for Google ID tokens."""
    url = urllib.parse.urljoin(host, '/auth/info/googleidtoken')
    params = {
        'key': api_key
    }
    headers = {
        'Authorization': 'Bearer {}'.format(id_token)
    }

    response = requests.get(url, params=params, headers=headers)

    response.raise_for_status()
    return response.text


def main(host, api_key, client_secrets_file, extra_args):
    id_token = get_id_token(client_secrets_file, extra_args)
    response = make_request(host, api_key, id_token)
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'host', help='Your API host, e.g. https://your-project.appspot.com.')
    parser.add_argument(
        'api_key', help='Your API key.')
    parser.add_argument(
        'client_secrets_file',
        help='The path to your OAuth2 client secrets file.')

    args = parser.parse_args()

    main(args.host, args.api_key, args.client_secrets_file, args)
