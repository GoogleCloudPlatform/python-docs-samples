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

"""Tests for dualtoken."""

import datetime

import pytest

import dualtoken


startTime = datetime.datetime.strptime("2022-09-13T00:00:00Z", "%Y-%m-%dT%H:%M:%S%z")
expiresTime = datetime.datetime.strptime("2022-09-13T12:00:00Z", "%Y-%m-%dT%H:%M:%S%z")
sessionID = "test-id"
data = "test-data"
ipRanges = "203.0.113.0/24,2001:db8:4a7f:a732/64"
headers = [
    {
        "name": "Foo",
        "value": "bar",
    },
    {
        "name": "BAZ",
        "value": "quux",
    },
]

with open("/tmp/example.key", "wb") as fp:
    fp.write(
        b"\x0c\x95\x1c\x9c\xb8.TR\xa6T!gXk\x9b\x1bS\x19\x83\xb7\xd6\x02|Zp\xc8\xca\x0e\x15Y0b\x9f\xb9\xf0\xbe\x1c\xda\xd7P\xb4J\xe5=k-nZ0\xd2\x7f1\xfe\n\x92\x01\x81|j#?\x98w\xd4"
    )

with open("/tmp/example.pub", "wb") as fp:
    fp.write(
        b"\x9f\xb9\xf0\xbe\x1c\xda\xd7P\xb4J\xe5=k-nZ0\xd2\x7f1\xfe\n\x92\x01\x81|j#?\x98w\xd4"
    )

with open("/tmp/shared.secret", "wb") as fp:
    fp.write(
        b"\x83\xf4\xa50\x82\xe2!b\xaa\xb0.\x99\xd8\xbe\xe0\xcbK\x11x3\xaa\xb5*\xc9\xacN\xc2\\\xda\xf96_"
    )


def test_sign_token_for_ed25519_url_prefix(capsys: pytest.LogCaptureFixture) -> None:
    expected = "URLPrefix=aHR0cDovLzEwLjIwLjMwLjQwLw~Expires=1663070400~Signature=OQLXEjnApFGJaGZ_jvp2R7VY5q3ic-HT3igFpi9iPsJRXtQuvPF4cxZUT-rtCqzteXx3vSRhk09FxgDQauO_DA"
    result = dualtoken.sign_token(
        base64_key=b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI=",
        signature_algorithm="ed25519",
        expiration_time=expiresTime,
        url_prefix="http://10.20.30.40/",
    )
    assert result == expected


def test_sign_token_for_ed25519_path_glob(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Expires=1663070400~Signature=9pBdD_6O6LB-4V67HZ_SOc2G_jIkSZ_tMsKnVqElmPlwKB_xDiW7DKAnv8L8CmweeZquaLFlnLogbMcIV8bNCQ"
    result = dualtoken.sign_token(
        base64_key=b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI=",
        signature_algorithm="ed25519",
        expiration_time=expiresTime,
        path_globs="/*",
    )
    assert result == expected


def test_sign_token_for_ed25519_full_path(capsys: pytest.LogCaptureFixture) -> None:
    expected = "FullPath~Expires=1663070400~Signature=X74OTNjtseIUmsab-YiOTZ8jyX_KG7v4YQWwcFpfFmjhzaX8NdweMc9Wglj8wxEsEW85g3_MBG3T9jzLZFQDCw"
    result = dualtoken.sign_token(
        base64_key=b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI=",
        signature_algorithm="ed25519",
        expiration_time=expiresTime,
        full_path="/example.m3u8",
    )
    assert result == expected


def test_sign_token_for_sha1_url_prefix(capsys: pytest.LogCaptureFixture) -> None:
    expected = "URLPrefix=aHR0cDovLzEwLjIwLjMwLjQwLw~Expires=1663070400~hmac=6f5b4bb82536810d5ee111cba3e534d49c6ac3cb"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha1",
        expiration_time=expiresTime,
        url_prefix="http://10.20.30.40/",
    )
    assert result == expected


def test_sign_token_for_sha1_path_glob(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Expires=1663070400~hmac=c1c446eea24faa31392519f975fea7eefb945625"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha1",
        expiration_time=expiresTime,
        path_globs="/*",
    )
    assert result == expected


def test_sign_token_for_sha1_full_path(capsys: pytest.LogCaptureFixture) -> None:
    expected = (
        "FullPath~Expires=1663070400~hmac=7af78177d6bc001d5626eefe387b1774a4a99ca2"
    )
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha1",
        expiration_time=expiresTime,
        full_path="/example.m3u8",
    )
    assert result == expected


def test_sign_token_for_sha256_url_prefix(capsys: pytest.LogCaptureFixture) -> None:
    expected = "URLPrefix=aHR0cDovLzEwLjIwLjMwLjQwLw~Expires=1663070400~hmac=409722313cf6d987da44bb360e60dccc3d79764520fc5e3b57654e1d4d2c862e"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha256",
        expiration_time=expiresTime,
        url_prefix="http://10.20.30.40/",
    )
    assert result == expected


def test_sign_token_for_sha256_path_globs(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Expires=1663070400~hmac=9439ecdd5c4919f76f915dea72afa85a045579794e63d8cda664f5a1140c8d93"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha256",
        expiration_time=expiresTime,
        path_globs="/*",
    )
    assert result == expected


def test_sign_token_for_sha256_full_path(capsys: pytest.LogCaptureFixture) -> None:
    expected = "FullPath~Expires=1663070400~hmac=365b41fd77297371d890fc9a56e4e3d3baa4c7afbd230a0e9a81c8e1bcab9420"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha256",
        expiration_time=expiresTime,
        full_path="/example.m3u8",
    )
    assert result == expected


def test_sign_token_for_ed25519_all_params(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Starts=1663027200~Expires=1663070400~SessionID=test-id~Data=test-data~Headers=Foo,BAZ~IPRanges=MjAzLjAuMTEzLjAvMjQsMjAwMTpkYjg6NGE3ZjphNzMyLzY0~Signature=A7u67hveGxGvP8KBWZlUuH0IsqhS4a2lcsXwy3uc4X3zaVuw7LY-2FQT1ZF8UxkSFAsDS3_0LYnXwXB2XdepDg"
    result = dualtoken.sign_token(
        base64_key=b"DJUcnLguVFKmVCFnWGubG1MZg7fWAnxacMjKDhVZMGI=",
        signature_algorithm="ed25519",
        start_time=startTime,
        expiration_time=expiresTime,
        path_globs="/*",
        session_id=sessionID,
        data=data,
        headers=headers,
        ip_ranges=ipRanges,
    )
    assert result == expected


def test_sign_token_for_sha1_all_params(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Starts=1663027200~Expires=1663070400~SessionID=test-id~Data=test-data~Headers=Foo,BAZ~IPRanges=MjAzLjAuMTEzLjAvMjQsMjAwMTpkYjg6NGE3ZjphNzMyLzY0~hmac=b8242e8b76cbfbbd61b3540ed0eb60a2ec2fdbdb"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha1",
        start_time=startTime,
        expiration_time=expiresTime,
        path_globs="/*",
        session_id=sessionID,
        data=data,
        headers=headers,
        ip_ranges=ipRanges,
    )
    assert result == expected


def test_sign_token_for_sha256_all_params(capsys: pytest.LogCaptureFixture) -> None:
    expected = "PathGlobs=/*~Starts=1663027200~Expires=1663070400~SessionID=test-id~Data=test-data~Headers=Foo,BAZ~IPRanges=MjAzLjAuMTEzLjAvMjQsMjAwMTpkYjg6NGE3ZjphNzMyLzY0~hmac=dda9c3d6f3b2e867a09fbb76209ea138dd81f8512210f970d1e92f90927bef4b"
    result = dualtoken.sign_token(
        base64_key=b"g_SlMILiIWKqsC6Z2L7gy0sReDOqtSrJrE7CXNr5Nl8=",
        signature_algorithm="sha256",
        start_time=startTime,
        expiration_time=expiresTime,
        path_globs="/*",
        session_id=sessionID,
        data=data,
        headers=headers,
        ip_ranges=ipRanges,
    )
    assert result == expected
