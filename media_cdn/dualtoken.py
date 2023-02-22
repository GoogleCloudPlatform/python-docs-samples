#!/usr/bin/env python
#
# Copyright 2022 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START  mediacdn_dual_token_sign_token]
import base64
import datetime
import hashlib
import hmac

import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519


def base64_encoder(value: bytes) -> str:
    """
    Returns a base64-encoded string compatible with Media CDN.

    Media CDN uses URL-safe base64 encoding and strips off the padding at the
    end.
    """
    encoded_bytes = base64.urlsafe_b64encode(value)
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str.rstrip("=")


def sign_token(
    base64_key: bytes,
    signature_algorithm: str,
    start_time: datetime.datetime = None,
    expiration_time: datetime.datetime = None,
    url_prefix: str = None,
    full_path: str = None,
    path_globs: str = None,
    session_id: str = None,
    data: str = None,
    headers: str = None,
    ip_ranges: str = None,
) -> str:
    """Gets the Signed URL Suffix string for the Media CDN' Short token URL requests.
    One of (`url_prefix`, `full_path`, `path_globs`) must be included in each input.
    Args:
        base64_key: Secret key as a base64 encoded string.
        signature_algorithm: Algorithm can be either `SHA1` or `SHA256` or `Ed25519`.
        start_time: Start time as a UTC datetime object.
        expiration_time: Expiration time as a UTC datetime object. If None, an expiration time 1 hour from now will be used.
        url_prefix: the URL prefix to sign, including protocol.
                    For example: http://example.com/path/ for URLs under /path or http://example.com/path?param=1
        full_path:  A full path to sign, starting with the first '/'.
                    For example: /path/to/content.mp4
        path_globs: a set of ','- or '!'-delimited path glob strings.
                    For example: /tv/*!/film/* to sign paths starting with /tv/ or /film/ in any URL.
        session_id: a unique identifier for the session
        data: data payload to include in the token
        headers: header name and value to include in the signed token in name=value format.  May be specified more than once.
                    For example: [{'name': 'foo', 'value': 'bar'}, {'name': 'baz', 'value': 'qux'}]
        ip_ranges: A list of comma separated ip ranges. Both IPv4 and IPv6 ranges are acceptable.
                    For example: "203.0.113.0/24,2001:db8:4a7f:a732/64"

    Returns:
        The Signed URL appended with the query parameters based on the
        specified URL prefix and configuration.
    """

    decoded_key = base64.urlsafe_b64decode(base64_key)
    algo = signature_algorithm.lower()

    # For most fields, the value we put in the token and the value we must sign
    # are the same.  The FullPath and Headers use a different string for the
    # value to be signed compared to the token.  To illustrate this difference,
    # we'll keep the token and the value to be signed separate.
    tokens = []
    to_sign = []

    # check for `full_path` or `path_globs` or `url_prefix`
    if full_path:
        tokens.append("FullPath")
        to_sign.append(f"FullPath={full_path}")
    elif path_globs:
        path_globs = path_globs.strip()
        field = f"PathGlobs={path_globs}"
        tokens.append(field)
        to_sign.append(field)
    elif url_prefix:
        field = "URLPrefix=" + base64_encoder(url_prefix.encode("utf-8"))
        tokens.append(field)
        to_sign.append(field)
    else:
        raise ValueError(
            "User Input Missing: One of `url_prefix`, `full_path` or `path_globs` must be specified"
        )

    # check & parse optional params
    if start_time:
        epoch_duration = start_time.astimezone(
            tz=datetime.timezone.utc
        ) - datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
        field = f"Starts={int(epoch_duration.total_seconds())}"
        tokens.append(field)
        to_sign.append(field)

    if not expiration_time:
        expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        epoch_duration = expiration_time.astimezone(
            tz=datetime.timezone.utc
        ) - datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    else:
        epoch_duration = expiration_time.astimezone(
            tz=datetime.timezone.utc
        ) - datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    field = f"Expires={int(epoch_duration.total_seconds())}"
    tokens.append(field)
    to_sign.append(field)

    if session_id:
        field = f"SessionID={session_id}"
        tokens.append(field)
        to_sign.append(field)

    if data:
        field = f"Data={data}"
        tokens.append(field)
        to_sign.append(field)

    if headers:
        header_names = []
        header_pairs = []
        for each in headers:
            header_names.append(each["name"])
            header_pairs.append("%s=%s" % (each["name"], each["value"]))
        tokens.append(f"Headers={','.join(header_names)}")
        to_sign.append(f"Headers={','.join(header_pairs)}")

    if ip_ranges:
        field = f"IPRanges={base64_encoder(ip_ranges.encode('ascii'))}"
        tokens.append(field)
        to_sign.append(field)

    # generating token
    to_sign = "~".join(to_sign)
    to_sign_bytes = to_sign.encode("utf-8")
    if algo == "ed25519":
        digest = ed25519.Ed25519PrivateKey.from_private_bytes(decoded_key).sign(
            to_sign_bytes
        )
        tokens.append("Signature=" + base64_encoder(digest))
    elif algo == "sha256":
        signature = hmac.new(
            decoded_key, to_sign_bytes, digestmod=hashlib.sha256
        ).hexdigest()
        tokens.append("hmac=" + signature)
    elif algo == "sha1":
        signature = hmac.new(
            decoded_key, to_sign_bytes, digestmod=hashlib.sha1
        ).hexdigest()
        tokens.append("hmac=" + signature)
    else:
        raise ValueError(
            "Input Missing Error: `signature_algorithm` can only be one of `sha1`, `sha256` or `ed25519`"
        )
    return "~".join(tokens)
# [end  mediacdn_dual_token_sign_token]

