#!/usr/bin/env python
#
# Copyright 2022 Google, Inc.
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

import pytest

import snippets


EPOCH_TIME = 1650848400


def test_sign_url(capsys: pytest.LogCaptureFixture) -> None:
    results = []
    results.append(
        snippets.sign_url(
            "http://35.186.234.33/index.html",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    results.append(
        snippets.sign_url(
            "http://www.example.com/",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    results.append(
        snippets.sign_url(
            "http://www.example.com/some/path?some=query&another=param",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    assert results[0] == (
        "http://35.186.234.33/index.html?Expires=1650848400&KeyName=my-key&"
        "Signature=16-oE9GZ5U9S_LYrW8RplZhvMfI7RGtGRY0C-Ahh6YAwiJ0UaEi6rQuPxfm6R-cBPfs8MwRGiu2fAoS1JOoKCA=="
    )
    assert results[1] == (
        "http://www.example.com/?Expires=1650848400&KeyName=my-key&"
        "Signature=QhWcq48iCRTJFayWexw929QRxjOxE8ZPSQ38ybTxLhu77hmS_JB6GSougMu_-ejS_ZiGguqxT-HfgSFuy3f5DQ=="
    )
    assert results[2] == (
        "http://www.example.com/some/path?some=query&another=param&Expires="
        "1650848400&KeyName=my-key&Signature=Li_D6rxUh1Kj54JbmUuAms2wmjJHJUcMXJHgYxjL4LqYH02wSX-4gCayXgklNSDpfBfSHnbdC_wvcdyXvADGDw=="
    )


def test_sign_url_prefix(capsys: pytest.LogCaptureFixture) -> None:
    results = []
    results.append(
        snippets.sign_url_prefix(
            "http://35.186.234.33/index.html",
            "http://35.186.234.33/",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    results.append(
        snippets.sign_url_prefix(
            "http://www.example.com/",
            "http://www.example.com/",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    results.append(
        snippets.sign_url_prefix(
            "http://www.example.com/some/path?some=query&another=param",
            "http://www.example.com/some/",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    assert results[0] == (
        "http://35.186.234.33/index.html?URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMv&"
        "Expires=1650848400&KeyName=my-key&"
        "Signature=mR4jNsWVn39ofSC5425SXwZVzHAAixemdcRGHgPuO1V1Fl7lJs2Ws5aPOGp-MhbDinFYUkutHh-I9c5Du4jtAA=="
    )
    assert results[1] == (
        "http://www.example.com/?URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS8=&"
        "Expires=1650848400&KeyName=my-key&"
        "Signature=gFGKa4T8Fn1GiTMp1VBd6sSfjRKcPEgTB1k8mn48yXyzg4-Dfbrk-HJeYFGFznZvkF_eSPg1K03hqbMDkFTiAg=="
    )
    assert results[2] == (
        "http://www.example.com/some/path?some=query&another=param&"
        "URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9zb21lLw==&"
        "Expires=1650848400&KeyName=my-key&"
        "Signature=pVN8HKc6Be-PDczd9NjqSui3HHaoCLUN5iDv6JhQ77uKigsCih6z_cMTGjeXhgGASh1zr-ZPrOnxWJxxGWxsBg=="
    )


def test_sign_cookie(capsys: pytest.LogCaptureFixture) -> None:
    results = []
    results.append(
        snippets.sign_cookie(
            "http://35.186.234.33/index.html",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    results.append(
        snippets.sign_cookie(
            "http://www.example.com/foo/",
            "my-key",
            "BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=",
            datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        )
    )
    assert results[0] == (
        "Edge-Cache-Cookie=URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMvaW5kZXguaHRtbA==:"
        "Expires=1650848400:KeyName=my-key:"
        "Signature=kTJ4QVEax5TZmxypq8pnIkjky-s_UtKGPSCd-nxqMYfwqr5HunAy-7XumWc3asRCHI2_ikVQXs7IDXJ9gV28Dg=="
    )
    assert results[1] == (
        "Edge-Cache-Cookie=URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9mb28v:"
        "Expires=1650848400:KeyName=my-key:"
        "Signature=I0BnupL1tKbXklf1rK50nlC9JMh4HBLogTKByatOFRvALofT159BegB26Z2WmrI-ZAgAp8Q-1__bWtFdMAqCAA=="
    )


def test_sign_token(capsys: pytest.LogCaptureFixture) -> None:
    results = [
        snippets.sign_token(
            url_prefix="http://35.186.234.33",
            base64_key=b"9koFqysqLzTsU5Mm7BDsVjOjDqN8RRrmsu3Oojxj7mo=",
            encryption_algorithm="sha1",
            expiration_time=datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        ),
        snippets.sign_token(
            url_prefix="http://www.example.com",
            base64_key=b"o7SD7eS/5q0ZNEVPKkPRAo6Yl3aPFXCh62Kyez1ygIQ=",
            encryption_algorithm="sha1",
            expiration_time=datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        ),
        snippets.sign_token(
            url_prefix="http://www.example.com",
            base64_key=b"dhs2goW4rKqaYap+xcLCh2gYJIZQv9p1R1vHvRGH4CU=",
            encryption_algorithm="sha256",
            expiration_time=datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        ),
        snippets.sign_token(
            url_prefix="http://0.0.0.0/",
            base64_key=b"Auo-t35Q1R_pk7sn2J6m_dhsMn-4Lbdlk-6qmmkxdFY=",
            encryption_algorithm="ed25519",
            expiration_time=datetime.datetime.utcfromtimestamp(EPOCH_TIME),
        ),
        snippets.sign_token(
            url_prefix="http://34.104.35.20/",
            encryption_algorithm="ed25519",
            base64_key=b"Auo-t35Q1R_pk7sn2J6m_dhsMn-4Lbdlk-6qmmkxdFY=",
            expiration_time=datetime.datetime.utcfromtimestamp(1664290336),
        ),
    ]
    print(results)
    assert results[0] == (
        "URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzM~Expires=1650848400"
        "~hmac=88d75457e5e729234460b11c7bdff0138222ed3a"
    )
    assert results[1] == (
        "URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbQ~Expires=1650848400"
        "~hmac=9103fd35ef2b628955ac0ba0cf1f16e1e7efd1da"
    )
    assert results[2] == (
        "URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbQ~Expires=1650848400"
        "~hmac=adf7ec51554ed1ba0d4806ba79ea36cb23680a41cb38a46b77b6359680400837"
    )
    assert results[3] == (
        "URLPrefix=aHR0cDovLzAuMC4wLjAv~Expires=1650848400"
        "~Signature=HXJewEzhm6Dda3FlsyaXa_6aCR6CPkz6SQGNApFNZp2AVxb9g96bGtZtmiwRatmrvLOM1pibMO3OeDp3za9oDg=="
    )
    assert results[4] == (
        "URLPrefix=aHR0cDovLzM0LjEwNC4zNS4yMC8~Expires=1664290336"
        "~Signature=NSU1VX2IzgZv24cOObQ2-U_R0uHEwyK9PxGFo41wiFKTfnNo60-vkia-tis0IHPjanwtg53pRkumRhqu_iJGCw=="
    )
    assert snippets.sign_token(
        path_globs="/shankar/*",
        encryption_algorithm="ed25519",
        base64_key=b"Auo-t35Q1R_pk7sn2J6m_dhsMn-4Lbdlk-6qmmkxdFY=",
        expiration_time=datetime.datetime.utcfromtimestamp(1664290336),
    ) == (
        "PathGlobs=/shankar/*"
        "~Expires=1664290336"
        "~Signature=W9A9DSHa3bIE3S_Z4xHFmHkCFLCfOxgVqSnkPI6srIRyzHTX1Yc3LZi0F5Ec3PQeZyG-UiyA-mUzd5jOMhUsCw=="
    )
    assert snippets.sign_token(
        url_prefix="http://34.104.35.20/",
        encryption_algorithm="ed25519",
        base64_key=b"Auo-t35Q1R_pk7sn2J6m_dhsMn-4Lbdlk-6qmmkxdFY=",
        expiration_time=datetime.datetime.utcfromtimestamp(1664290336),
    ) == (
        "URLPrefix=aHR0cDovLzM0LjEwNC4zNS4yMC8"
        "~Expires=1664290336"
        "~Signature=NSU1VX2IzgZv24cOObQ2-U_R0uHEwyK9PxGFo41wiFKTfnNo60-vkia-tis0IHPjanwtg53pRkumRhqu_iJGCw=="
    )
