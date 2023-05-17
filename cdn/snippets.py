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
from datetime import datetime
import hashlib
import hmac
from urllib.parse import parse_qs, urlsplit


# [START cloudcdn_sign_url]
def sign_url(
    url: str,
    key_name: str,
    base64_key: str,
    expiration_time: datetime,
) -> str:
    """Gets the Signed URL string for the specified URL and configuration.

    Args:
        url: URL to sign.
        key_name: name of the signing key.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified configuration.
    """
    stripped_url = url.strip()
    parsed_url = urlsplit(stripped_url)
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    epoch = datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    url_to_sign = f"{stripped_url}{'&' if query_params else '?'}Expires={expiration_timestamp}&KeyName={key_name}"

    digest = hmac.new(decoded_key, url_to_sign.encode("utf-8"), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode("utf-8")

    return f"{url_to_sign}&Signature={signature}"


# [END cloudcdn_sign_url]


# [START cloudcdn_sign_url_prefix]
def sign_url_prefix(
    url: str,
    url_prefix: str,
    key_name: str,
    base64_key: str,
    expiration_time: datetime,
) -> str:
    """Gets the Signed URL string for the specified URL prefix and configuration.

    Args:
        url: URL of request.
        url_prefix: URL prefix to sign.
        key_name: name of the signing key.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified URL prefix and configuration.
    """
    stripped_url = url.strip()
    parsed_url = urlsplit(stripped_url)
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    encoded_url_prefix = base64.urlsafe_b64encode(
        url_prefix.strip().encode("utf-8")
    ).decode("utf-8")
    epoch = datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy = f"URLPrefix={encoded_url_prefix}&Expires={expiration_timestamp}&KeyName={key_name}"

    digest = hmac.new(decoded_key, policy.encode("utf-8"), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode("utf-8")

    return f"{stripped_url}{'&' if query_params else '?'}{policy}&Signature={signature}"


# [END cloudcdn_sign_url_prefix]


# [START cloudcdn_sign_cookie]
def sign_cookie(
    url_prefix: str,
    key_name: str,
    base64_key: str,
    expiration_time: datetime,
) -> str:
    """Gets the Signed cookie value for the specified URL prefix and configuration.

    Args:
        url_prefix: URL prefix to sign.
        key_name: name of the signing key.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time.

    Returns:
        Returns the Cloud-CDN-Cookie value based on the specified configuration.
    """
    encoded_url_prefix = base64.urlsafe_b64encode(
        url_prefix.strip().encode("utf-8")
    ).decode("utf-8")
    epoch = datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy = f"URLPrefix={encoded_url_prefix}:Expires={expiration_timestamp}:KeyName={key_name}"

    digest = hmac.new(decoded_key, policy.encode("utf-8"), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode("utf-8")

    signed_policy = f"Cloud-CDN-Cookie={policy}:Signature={signature}"

    return signed_policy


# [END cloudcdn_sign_cookie]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command")

    sign_url_parser = subparsers.add_parser(
        "sign-url", help="Sign a URL to grant temporary authorized access."
    )
    sign_url_parser.add_argument("url", help="The URL to sign.")
    sign_url_parser.add_argument("key_name", help="Key name for the signing key.")
    sign_url_parser.add_argument("base64_key", help="The base64 encoded signing key.")
    sign_url_parser.add_argument(
        "expiration_time",
        type=lambda d: datetime.utcfromtimestamp(float(d)),
        help="Expiration time expessed as seconds since the epoch.",
    )

    sign_url_prefix_parser = subparsers.add_parser(
        "sign-url-prefix",
        help="Sign a URL prefix to grant temporary authorized access.",
    )
    sign_url_prefix_parser.add_argument("url", help="The request URL.")
    sign_url_prefix_parser.add_argument("url_prefix", help="The URL prefix to sign.")
    sign_url_prefix_parser.add_argument(
        "key_name", help="Key name for the signing key."
    )
    sign_url_prefix_parser.add_argument(
        "base64_key", help="The base64 encoded signing key."
    )
    sign_url_prefix_parser.add_argument(
        "expiration_time",
        type=lambda d: datetime.utcfromtimestamp(float(d)),
        help="Expiration time expessed as seconds since the epoch.",
    )

    sign_cookie_parser = subparsers.add_parser(
        "sign-cookie",
        help="Generate a signed cookie to grant temporary authorized access.",
    )
    sign_cookie_parser.add_argument("url_prefix", help="The URL prefix to sign.")
    sign_cookie_parser.add_argument("key_name", help="Key name for the signing key.")
    sign_cookie_parser.add_argument(
        "base64_key", help="The base64 encoded signing key."
    )
    sign_cookie_parser.add_argument(
        "expiration_time",
        type=lambda d: datetime.utcfromtimestamp(float(d)),
        help="Expiration time expressed as seconds since the epoch.",
    )

    args = parser.parse_args()

    if args.command == "sign-url":
        print(sign_url(args.url, args.key_name, args.base64_key, args.expiration_time))
    elif args.command == "sign-url-prefix":
        print(
            sign_url_prefix(
                args.url,
                args.url_prefix,
                args.key_name,
                args.base64_key,
                args.expiration_time,
            )
        )
    elif args.command == "sign-cookie":
        print(
            sign_cookie(
                args.url_prefix, args.key_name, args.base64_key, args.expiration_time
            )
        )
