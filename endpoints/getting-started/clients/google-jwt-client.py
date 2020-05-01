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


# [START endpoints_generate_jwt_sa]
def generate_jwt(sa_keyfile,
                 sa_email='account@project-id.iam.gserviceaccount.com',
                 audience='your-service-name',
                 expiry_length=3600):

    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud':  audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt
# [END endpoints_generate_jwt_sa]


# [START endpoints_jwt_request]
def make_jwt_request(signed_jwt, url='https://your-endpoint.com'):
    """Makes an authorized request to the endpoint"""
    headers = {
        'Authorization': 'Bearer {}'.format(signed_jwt.decode('utf-8')),
        'content-type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(response.status_code, response.content)
    response.raise_for_status()

# [END endpoints_jwt_request]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'host', help='Your API host, e.g. https://your-project.appspot.com.')
    parser.add_argument(
        'audience', help='The aud entry for the JWT')
    parser.add_argument(
        'sa_path',
        help='The path to your service account json file.')
    parser.add_argument(
        'sa_email',
        help='The email address for the service account.')

    args = parser.parse_args()

    expiry_length = 3600
    keyfile_jwt = generate_jwt(args.sa_path,
                               args.sa_email,
                               args.audience,
                               expiry_length)
    make_jwt_request(keyfile_jwt, args.host)
