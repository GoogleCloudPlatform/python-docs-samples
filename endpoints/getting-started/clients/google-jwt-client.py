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

"""Example of calling a Google Cloud Endpoint API with a JWT signed by
a Google API Service Account."""

import argparse
import time

import google.auth.crypt
import google.auth.jwt
import requests
from six.moves import urllib


def generate_jwt(service_account_file):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    # Note: this sample shows how to manually create the JWT for the purposes
    # of showing how the authentication works, but you can use
    # google.auth.jwt.Credentials to automatically create the JWT.
    #   http://google-auth.readthedocs.io/en/latest/reference
    #   /google.auth.jwt.html#google.auth.jwt.Credentials

    signer = google.auth.crypt.RSASigner.from_service_account_file(
        service_account_file)

    now = int(time.time())
    expires = now + 3600  # One hour in seconds

    payload = {
        'iat': now,
        'exp': expires,
        # aud must be either your Endpoints service name or match a value
        # specified in 'x-google-audience' in the security configuration in your
        # OpenAPI document.
        'aud': 'echo.endpoints.sample.google.com',
        # iss must be the service account email and it must match the value
        # specified in 'x-google-issuer' in the security configuration in your
        # OpenAPI document.
        'iss': 'service-1@example-project-12345.iam.gserviceaccount.com',
        # sub and email must match iss.
        'sub': 'service-1@example-project-12345.iam.gserviceaccount.com',
        'email': 'service-1@example-project-12345.iam.gserviceaccount.com'
    }

    jwt = google.auth.jwt.encode(signer, payload).decode('UTF-8')

    return jwt


def make_request(host, api_key, signed_jwt):
    """Makes a request to the auth info endpoint for Google JWTs."""
    url = urllib.parse.urljoin(host, '/auth/info/googlejwt')
    params = {
        'key': api_key
    }
    headers = {
        'Authorization': 'Bearer {}'.format(signed_jwt)
    }

    response = requests.get(url, params=params, headers=headers)

    response.raise_for_status()
    return response.text


def main(host, api_key, service_account_file):
    signed_jwt = generate_jwt(service_account_file)
    response = make_request(host, api_key, signed_jwt)
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
        'service_account_file',
        help='The path to your service account json file.')

    args = parser.parse_args()

    main(args.host, args.api_key, args.service_account_file)
