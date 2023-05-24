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

"""Tests for snippets."""

import datetime

import snippets


def test_sign_url():
    assert (
        snippets.sign_url(
            "http://35.186.234.33/index.html",
            "my-key",
            "nZtRohdNF9m3cKM24IcK4w==",
            datetime.datetime.utcfromtimestamp(1549751401),
        )
        == "http://35.186.234.33/index.html?Expires=1549751401&KeyName=my-key&Signature=CRFqQnVfFyiUyR63OQf-HRUpIwc="
    )

    assert (
        snippets.sign_url(
            "http://www.example.com/",
            "my-key",
            "nZtRohdNF9m3cKM24IcK4w==",
            datetime.datetime.utcfromtimestamp(1549751401),
        )
        == "http://www.example.com/?Expires=1549751401&KeyName=my-key&Signature=OqDUFfHpN5Vxga6r80bhsgxKves="
    )
    assert (
        snippets.sign_url(
            "http://www.example.com/some/path?some=query&another=param",
            "my-key",
            "nZtRohdNF9m3cKM24IcK4w==",
            datetime.datetime.utcfromtimestamp(1549751401),
        )
        == "http://www.example.com/some/path?some=query&another=param&Expires=1549751401&KeyName=my-key&Signature=9Q9TCxSju8-W5nUkk5CuTrun2_o="
    )


def test_sign_url_prefix():
    assert snippets.sign_url_prefix(
        "http://35.186.234.33/index.html",
        "http://35.186.234.33/",
        "my-key",
        "nZtRohdNF9m3cKM24IcK4w==",
        datetime.datetime.utcfromtimestamp(1549751401),
    ) == (
        "http://35.186.234.33/index.html?URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMv&"
        "Expires=1549751401&KeyName=my-key&Signature=j7HYgoQ8dIOVsW3Rw4cpkjWfRMA="
    )
    assert snippets.sign_url_prefix(
        "http://www.example.com/",
        "http://www.example.com/",
        "my-key",
        "nZtRohdNF9m3cKM24IcK4w==",
        datetime.datetime.utcfromtimestamp(1549751401),
    ) == (
        "http://www.example.com/?URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS8=&"
        "Expires=1549751401&KeyName=my-key&Signature=UdT5nVks6Hh8QFMJI9kmXuXYBk0="
    )
    assert snippets.sign_url_prefix(
        "http://www.example.com/some/path?some=query&another=param",
        "http://www.example.com/some/",
        "my-key",
        "nZtRohdNF9m3cKM24IcK4w==",
        datetime.datetime.utcfromtimestamp(1549751401),
    ) == (
        "http://www.example.com/some/path?some=query&another=param&"
        "URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9zb21lLw==&"
        "Expires=1549751401&KeyName=my-key&Signature=3th4ThmpS95I1TAKYyYSCSq3dnQ="
    )


def test_sign_cookie():
    assert (
        snippets.sign_cookie(
            "http://35.186.234.33/index.html",
            "my-key",
            "nZtRohdNF9m3cKM24IcK4w==",
            datetime.datetime.utcfromtimestamp(1549751401),
        )
        == "Cloud-CDN-Cookie=URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMvaW5kZXguaHRtbA==:Expires=1549751401:KeyName=my-key:Signature=uImwlOBCPs91mlCyG9vyyZRrNWU="
    )

    assert (
        snippets.sign_cookie(
            "http://www.example.com/foo/",
            "my-key",
            "nZtRohdNF9m3cKM24IcK4w==",
            datetime.datetime.utcfromtimestamp(1549751401),
        )
        == "Cloud-CDN-Cookie=URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9mb28v:Expires=1549751401:KeyName=my-key:Signature=Z9uYAu73YHioRScZDxnP-TnS274="
    )
