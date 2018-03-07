#!/usr/bin/env python
#
# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform operations on data (content)
when using Google Cloud CDN (Content Delivery Network).

For more information, see the README.md under /cdn and the documentation
at https://cloud.google.com/cdn/docs.
"""

import argparse
import base64
import datetime
import hashlib
import hmac

# Python 2 & 3 compatibility
try:
    from urllib.parse import urlsplit, parse_qs
except ImportError:
    from urlparse import urlsplit, parse_qs

# [BEGIN sign_url]
def sign_url(url, key_name, key, expiration_time):
    """Gets the Signed URL string for the specified URL and configuration.

    Args:
        url: URL to sign as a string.
        key_name: name of the signing key as a string.
        key: signing key as a urlsafe base64 encoded string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified configuration.  Roughly of the form:
        {url}{separator}Expires={expiration}&KeyName={key_name}&Signature={signature}

    """
    stripped_url = url.strip()
    parsed_url = urlsplit(stripped_url)
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(key)

    url_to_sign = '{url}{separator}Expires={expires}&KeyName={key_name}'.format(
            url=stripped_url,
            separator='&' if query_params else '?',
            expires=expiration_timestamp,
            key_name=key_name)

    signature = base64.urlsafe_b64encode(
            hmac.new(decoded_key, url_to_sign, hashlib.sha1).digest())

    return '{url}&Signature={signature}'.format(
            url=url_to_sign, signature=signature)
# [END sign_url]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    sign_url_parser = subparsers.add_parser(
            'sign-url',
            help="Sign a URL to grant temporary authorized access.")
    sign_url_parser.add_argument(
            'url', help='The URL to sign')
    sign_url_parser.add_argument(
            'key_name',
            help='Key name for the authorization secret key.')
    sign_url_parser.add_argument(
            'key',
            help='The base64 encoded secret key value to use for signing.')
    sign_url_parser.add_argument(
            'expiration_time',
            type=lambda d: datetime.datetime.utcfromtimestamp(float(d)),
            help='Expiration time expessed as seconds since the epoch.')

    args = parser.parse_args()

    if args.command == 'sign-url':
        print(sign_url(args.url, args.key_name, args.key, args.expiration_time))

