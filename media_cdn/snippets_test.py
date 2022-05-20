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
    results.append(snippets.sign_url(
        'http://35.186.234.33/index.html',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    results.append(snippets.sign_url(
        'http://www.example.com/',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    results.append(snippets.sign_url(
        'http://www.example.com/some/path?some=query&another=param',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    assert results[0] == (
        'http://35.186.234.33/index.html?Expires=1650848400&KeyName=my-key&'
        'Signature=16-oE9GZ5U9S_LYrW8RplZhvMfI7RGtGRY0C-Ahh6YAwiJ0UaEi6rQuPxfm6R-cBPfs8MwRGiu2fAoS1JOoKCA==')
    assert results[1] == (
        'http://www.example.com/?Expires=1650848400&KeyName=my-key&'
        'Signature=QhWcq48iCRTJFayWexw929QRxjOxE8ZPSQ38ybTxLhu77hmS_JB6GSougMu_-ejS_ZiGguqxT-HfgSFuy3f5DQ==')
    assert results[2] == (
        'http://www.example.com/some/path?some=query&another=param&Expires='
        '1650848400&KeyName=my-key&Signature=Li_D6rxUh1Kj54JbmUuAms2wmjJHJUcMXJHgYxjL4LqYH02wSX-4gCayXgklNSDpfBfSHnbdC_wvcdyXvADGDw==')


def test_sign_url_prefix(capsys: pytest.LogCaptureFixture) -> None:
    results = []
    results.append(snippets.sign_url_prefix(
        'http://35.186.234.33/index.html',
        'http://35.186.234.33/',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    results.append(snippets.sign_url_prefix(
        'http://www.example.com/',
        'http://www.example.com/',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    results.append(snippets.sign_url_prefix(
        'http://www.example.com/some/path?some=query&another=param',
        'http://www.example.com/some/',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    assert results[0] == (
        'http://35.186.234.33/index.html?URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMv&'
        'Expires=1650848400&KeyName=my-key&'
        'Signature=mR4jNsWVn39ofSC5425SXwZVzHAAixemdcRGHgPuO1V1Fl7lJs2Ws5aPOGp-MhbDinFYUkutHh-I9c5Du4jtAA==')
    assert results[1] == (
        'http://www.example.com/?URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS8=&'
        'Expires=1650848400&KeyName=my-key&'
        'Signature=gFGKa4T8Fn1GiTMp1VBd6sSfjRKcPEgTB1k8mn48yXyzg4-Dfbrk-HJeYFGFznZvkF_eSPg1K03hqbMDkFTiAg==')
    assert results[2] == (
        'http://www.example.com/some/path?some=query&another=param&'
        'URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9zb21lLw==&'
        'Expires=1650848400&KeyName=my-key&'
        'Signature=pVN8HKc6Be-PDczd9NjqSui3HHaoCLUN5iDv6JhQ77uKigsCih6z_cMTGjeXhgGASh1zr-ZPrOnxWJxxGWxsBg==')


def test_sign_cookie(capsys: pytest.LogCaptureFixture) -> None:
    results = []
    results.append(snippets.sign_cookie(
        'http://35.186.234.33/index.html',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    results.append(snippets.sign_cookie(
        'http://www.example.com/foo/',
        'my-key',
        'BxwXXNjeGaoWqjr7GHEymRJkP4SaOC12dTGixk7Yr8I=',
        datetime.datetime.utcfromtimestamp(EPOCH_TIME)))
    assert results[0] == (
        'Edge-Cache-Cookie=URLPrefix=aHR0cDovLzM1LjE4Ni4yMzQuMzMvaW5kZXguaHRtbA==:'
        'Expires=1650848400:KeyName=my-key:'
        'Signature=kTJ4QVEax5TZmxypq8pnIkjky-s_UtKGPSCd-nxqMYfwqr5HunAy-7XumWc3asRCHI2_ikVQXs7IDXJ9gV28Dg==')
    assert results[1] == (
        'Edge-Cache-Cookie=URLPrefix=aHR0cDovL3d3dy5leGFtcGxlLmNvbS9mb28v:'
        'Expires=1650848400:KeyName=my-key:'
        'Signature=I0BnupL1tKbXklf1rK50nlC9JMh4HBLogTKByatOFRvALofT159BegB26Z2WmrI-ZAgAp8Q-1__bWtFdMAqCAA==')
