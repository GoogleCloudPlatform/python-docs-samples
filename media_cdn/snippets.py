#!/usr/bin/env python
#
# Copyright 2023 Google, Inc.
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
when using Google Cloud Media CDN.

For more information, see the README.md under /media-cdn and the documentation
at https://cloud.google.com/media-cdn/docs.
"""

# [START mediacdn_sign_url]
# [START mediacdn_sign_cookie]
# [START mediacdn_sign_url_prefix]
import base64
import datetime

import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519


from six.moves import urllib

# [END mediacdn_sign_cookie]
# [END mediacdn_sign_url]
# [END mediacdn_sign_url_prefix]


# [START mediacdn_sign_url]
def sign_url(url: str, key_name: str, base64_key: str, expiration_time: datetime.datetime) -> str:
    """Gets the Signed URL string for the specified URL and configuration.

    Args:
        url: URL to sign as a string.
        key_name: name of the signing key as a string.
        base64_key: signing key as a base64 encoded byte string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified configuration.
    """
    stripped_url = url.strip()
    parsed_url = urllib.parse.urlsplit(stripped_url)
    query_params = urllib.parse.parse_qs(
        parsed_url.query, keep_blank_values=True)
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    url_pattern = u'{url}{separator}Expires={expires}&KeyName={key_name}'

    url_to_sign = url_pattern.format(
            url=stripped_url,
            separator='&' if query_params else '?',
            expires=expiration_timestamp,
            key_name=key_name)

    digest = ed25519.Ed25519PrivateKey.from_private_bytes(
        decoded_key).sign(url_to_sign.encode('utf-8'))
    signature = base64.urlsafe_b64encode(digest).decode('utf-8')
    signed_url = u'{url}&Signature={signature}'.format(
            url=url_to_sign, signature=signature)

    return signed_url
# [END mediacdn_sign_url]


# [START mediacdn_sign_url_prefix]
def sign_url_prefix(url: str, url_prefix: str, key_name: str, base64_key: str, expiration_time: datetime.datetime) -> str:
    """Gets the Signed URL string for the specified URL prefix and configuration.

    Args:
        url: URL of request.
        url_prefix: URL prefix to sign as a string.
        key_name: name of the signing key as a string.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified URL prefix and configuration.
    """
    stripped_url = url.strip()
    parsed_url = urllib.parse.urlsplit(stripped_url)
    query_params = urllib.parse.parse_qs(
        parsed_url.query, keep_blank_values=True)
    encoded_url_prefix = base64.urlsafe_b64encode(
            url_prefix.strip().encode('utf-8')).decode('utf-8')
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy_pattern = u'URLPrefix={encoded_url_prefix}&Expires={expires}&KeyName={key_name}'
    policy = policy_pattern.format(
            encoded_url_prefix=encoded_url_prefix,
            expires=expiration_timestamp,
            key_name=key_name)

    digest = ed25519.Ed25519PrivateKey.from_private_bytes(
        decoded_key).sign(policy.encode('utf-8'))
    signature = base64.urlsafe_b64encode(digest).decode('utf-8')
    signed_url = u'{url}{separator}{policy}&Signature={signature}'.format(
            url=stripped_url,
            separator='&' if query_params else '?',
            policy=policy,
            signature=signature)
    return signed_url
# [END mediacdn_sign_url_prefix]


# [START mediacdn_sign_cookie]
def sign_cookie(url_prefix: str, key_name: str, base64_key: str, expiration_time: datetime.datetime) -> str:
    """Gets the Signed cookie value for the specified URL prefix and configuration.

    Args:
        url_prefix: URL prefix to sign as a string.
        key_name: name of the signing key as a string.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Edge-Cache-Cookie value based on the specified configuration.
    """
    encoded_url_prefix = base64.urlsafe_b64encode(
            url_prefix.strip().encode('utf-8')).decode('utf-8')
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy_pattern = u'URLPrefix={encoded_url_prefix}:Expires={expires}:KeyName={key_name}'
    policy = policy_pattern.format(
            encoded_url_prefix=encoded_url_prefix,
            expires=expiration_timestamp,
            key_name=key_name)

    digest = ed25519.Ed25519PrivateKey.from_private_bytes(
        decoded_key).sign(policy.encode('utf-8'))
    signature = base64.urlsafe_b64encode(digest).decode('utf-8')

    signed_policy = u'Edge-Cache-Cookie={policy}:Signature={signature}'.format(
            policy=policy, signature=signature)
    return signed_policy
# [END mediacdn_sign_cookie]
