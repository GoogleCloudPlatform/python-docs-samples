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

"""Example of generating a JWT signed from a service account file."""

import argparse
import json
import time

import google.auth.crypt
import google.auth.jwt

"""Max lifetime of the token (one hour, in seconds)."""
MAX_TOKEN_LIFETIME_SECS = 3600


def generate_jwt(service_account_file, issuer, audiences):
    """Generates a signed JSON Web Token using a Google API Service Account."""
    with open(service_account_file) as fh:
        service_account_info = json.load(fh)

    signer = google.auth.crypt.RSASigner.from_string(
        service_account_info['private_key'],
        service_account_info['private_key_id'])

    now = int(time.time())

    payload = {
        'iat': now,
        'exp': now + MAX_TOKEN_LIFETIME_SECS,
        # aud must match 'audience' in the security configuration in your
        # swagger spec. It can be any string.
        'aud': audiences,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec. It can be any string.
        'iss': issuer,
        # sub and email are mapped to the user id and email respectively.
        'sub': issuer,
        'email': 'user@example.com'
    }

    signed_jwt = google.auth.jwt.encode(signer, payload)
    return signed_jwt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--file',
                        help='The path to your service account json file.')
    parser.add_argument('--issuer', default='', help='issuer')
    parser.add_argument('--audiences', default='', help='audiences')

    args = parser.parse_args()

    signed_jwt = generate_jwt(args.file, args.issuer, args.audiences)
    print(signed_jwt.decode('utf-8'))
