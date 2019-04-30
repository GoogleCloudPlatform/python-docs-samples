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

"""Example of calling a simple Google Cloud Endpoint API."""

import argparse

import requests
from six.moves import urllib


def make_request(host, api_key, message):
    """Makes a request to the auth info endpoint for Google ID tokens."""
    url = urllib.parse.urljoin(host, 'echo')
    params = {
        'key': api_key
    }
    body = {
        'message': message
    }

    response = requests.post(url, params=params, json=body)

    response.raise_for_status()
    return response.text


def main(host, api_key, message):
    response = make_request(host, api_key, message)
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
        'message',
        help='Message to echo.')

    args = parser.parse_args()

    main(args.host, args.api_key, args.message)
