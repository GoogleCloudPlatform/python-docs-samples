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

import os
import re

from sentiment_analysis import analyze

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_pos(capsys):
    analyze(os.path.join(RESOURCES, 'pos.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert score * magnitude > 0


def test_neg(capsys):
    analyze(os.path.join(RESOURCES, 'neg.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert score * magnitude < 0


def test_mixed(capsys):
    analyze(os.path.join(RESOURCES, 'mixed.txt'))
    out, err = capsys.readouterr()
    score = float(re.search('score of (.+?) with', out).group(1))
    assert score <= 0.3
    assert score >= -0.3


def test_neutral(capsys):
    analyze(os.path.join(RESOURCES, 'neutral.txt'))
    out, err = capsys.readouterr()
    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
    assert magnitude <= 2.0
