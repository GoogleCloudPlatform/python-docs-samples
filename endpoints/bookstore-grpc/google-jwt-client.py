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

"""Example of generateing a JWT signed from a service account file."""

import argparse
import time

import oauth2client.crypt
from oauth2client.service_account import ServiceAccountCredentials


def generate_jwt(service_account_file, issuer, audiences):
    """Generates a signed JSON Web Token using a Google API Service Account."""
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_file)

    now = int(time.time())

    payload = {
        'iat': now,
        'exp': now + credentials.MAX_TOKEN_LIFETIME_SECS,
        # aud must match 'audience' in the security configuration in your
        # swagger spec. It can be any string.
        'aud': audiences,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec. It can be any string.
        'iss': issuer,
        # sub and email are mapped to the user id and email respectively.
        'sub': '12345678',
        'email': 'user@example.com'
    }

    signed_jwt = oauth2client.crypt.make_signed_jwt(
        credentials._signer, payload, key_id=credentials._private_key_id)

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
    print(signed_jwt)
