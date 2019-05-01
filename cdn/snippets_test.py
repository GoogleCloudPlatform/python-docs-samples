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


def test_sign_url(capsys):
    snippets.sign_url(
        'http://35.186.234.33/index.html',
        'my-key',
        'nZtRohdNF9m3cKM24IcK4w==',
        datetime.datetime.utcfromtimestamp(1549751401))
    snippets.sign_url(
        'http://www.example.com/',
        'my-key',
        'nZtRohdNF9m3cKM24IcK4w==',
        datetime.datetime.utcfromtimestamp(1549751401))
    snippets.sign_url(
        'http://www.example.com/some/path?some=query&another=param',
        'my-key',
        'nZtRohdNF9m3cKM24IcK4w==',
        datetime.datetime.utcfromtimestamp(1549751401))

    out, _ = capsys.readouterr()

    results = out.splitlines()
    assert results[0] == (
        'http://35.186.234.33/index.html?Expires=1549751401&KeyName=my-key&'
        'Signature=CRFqQnVfFyiUyR63OQf-HRUpIwc=')
    assert results[1] == (
        'http://www.example.com/?Expires=1549751401&KeyName=my-key&'
        'Signature=OqDUFfHpN5Vxga6r80bhsgxKves=')
    assert results[2] == (
        'http://www.example.com/some/path?some=query&another=param&Expires='
        '1549751401&KeyName=my-key&Signature=9Q9TCxSju8-W5nUkk5CuTrun2_o=')
