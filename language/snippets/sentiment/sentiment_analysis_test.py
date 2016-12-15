# Copyright 2016, Google, Inc.
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

import re

from sentiment_analysis import analyze


def test_pos(resource, capsys):
    analyze(resource('pos.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert score * magnitude > 0


def test_neg(resource, capsys):
    analyze(resource('neg.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert score * magnitude < 0


def test_mixed(resource, capsys):
    analyze(resource('mixed.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    assert score <= 0.3
    assert score >= -0.3


def test_neutral(resource, capsys):
    analyze(resource('neutral.txt'))
    out, err = capsys.readouterr()
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert magnitude <= 2.0
