#!/bin/python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.rom googleapiclient import discovery

"""Use a service account to access an IAP protected resource"""


def get_private_key(json_file_name):
    """Gets a service account's private key

    Args:
        json_file_name: the file containing the downloaded key information

    Returns:
        The private key from the file
    """

    import json

    with open(json_file_name, 'r') as f:
        json_key = f.read()

    key = json.loads(json_key)
    return key['private_key']


def build_claim(client_id, service_account):
    """Creates the necessary claim to request access to an IAP protected URL
    Args:
        client_id: the OAuth client ID. Available from API/Credentials console
        service_account: the service account email


    Returns:
        The claim
    """
    import time

    oauth_endpoint = 'https://www.googleapis.com/oauth2/v4/token'
    now = int(time.time())

    claim = {
        'iss': service_account,
        'target_audience': client_id,
        'iat': now,
        'exp': now + 3600,
        'aud': oauth_endpoint
    }

    return claim


def create_assertion(claim, private_key):
    """Creates an assertion - a signed claim of authorization

    Args:
        claim: the claim to send to the OAuth2 service (from build_claim)
        private_key: the service account's private key (in PEM format)

    Returns:
        The assertion
    """
    import jwt
    
    assertion = jwt.encode(
        claim,
        private_key,
        algorithm='RS256'
    )

    return assertion


def get_id_token(claim, private_key):
    """Gets an OpenID Connect token for the given private key

    Args:
        claim: the claim to send to the OAuth2 service (from build_claim)
        private_key: the service account's private key (in PEM format)

    Returns:
        An OpenID connect token to authenticate requests from the service acct
    """

    import json
    import requests

    assertion = create_assertion(claim, private_key)

    endpoint = claim['aud']
    grant_type = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

    response = requests.post(
        endpoint,
        data = {
            'grant_type': grant_type,
            'assertion': assertion
        }
    )

    print(response.text)

    id_token = response.json()['id_token']
    return id_token


def request(client_id, service_account, private_key, method, url, **kwargs):
    """Acts like requests.request, but includes IAP required authentication

    Args:
        client_id: the OAuth client ID. Available from API/Credentials console
        service_account: the service account email
        private_key: the service account's private key, in PEM format

        Remaining arguments are passed through to requests.request
            method: the HTTP method
            url: the address to access
            kwargs: other arguments to pass to requests.request

    Returns:
        The requests Response object from the request
    """

    import requests

    # Add Authorization header using service account and client information
    claim = build_claim(client_id, service_account)
    id_token = get_id_token(claim, private_key)

    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Authorization'] = 'Bearer {}'.format(id_token)

    # Make request with added Authorization header
    return requests.request(method, url, **kwargs)


def main():
    """Make a GET request to the IAP-protected URL using service account creds
    """

    import argparse

    parser = argparse.ArgumentParser(
        description='Call IAP protected resource with service account'
    )

    parser.add_argument('client_id', help="The protected site's client ID")
    parser.add_argument('service_account', help="The service account's email")
    parser.add_argument('key_file', help="The service account's key file")
    parser.add_argument('url', help="URL to access")

    args = parser.parse_args()

    private_key = get_private_key(args.key_file)

    response = request(
        args.client_id, args.service_account, private_key, 'GET', args.url
    )

    print('Status code: {} {}'.format(response.status_code, response.reason))
    print('Headers:')
    for key in response.headers:
        print('    {}: {}'.format(key, response.headers[key]))
    print('Body:')
    print(response.text)


if __name__ == '__main__':
    main()
