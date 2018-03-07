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
        'http://www.example.com/', 'my-key', 'd9hoKw==', datetime.datetime.max)

    out, _ = capsys.readouterr()

    assert out == ('http://www.example.com/?Expires=253402300800&'
                   'KeyName=my-key&Signature=w5FrhnkzGIrEabLP9HNxETNmS9U=')
