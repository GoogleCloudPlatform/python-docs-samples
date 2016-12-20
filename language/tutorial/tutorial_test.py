# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re

import tutorial


def test_neutral(capsys):
    tutorial.print_sentiment('reviews/bladerunner-neutral.txt')
    out, _ = capsys.readouterr()
    assert re.search(r'Sentence \d has a sentiment score of \d', out, re.I)
    assert re.search(
        r'Overall Sentiment: score of -?[0-2]\.?[0-9]? with '
        r'magnitude of [0-1]\.?[0-9]?', out, re.I)


def test_pos(capsys):
    tutorial.print_sentiment('reviews/bladerunner-pos.txt')
    out, _ = capsys.readouterr()
    assert re.search(r'Sentence \d has a sentiment score of \d', out, re.I)
    assert re.search(
        r'Overall Sentiment: score of [0-9]\.?[0-9]? with '
        r'magnitude of [0-9]\.?[0-9]?', out, re.I)


def test_neg(capsys):
    tutorial.print_sentiment('reviews/bladerunner-neg.txt')
    out, _ = capsys.readouterr()
    assert re.search(r'Sentence \d has a sentiment score of \d', out, re.I)
    assert re.search(
        r'Overall Sentiment: score of -[0-9]\.?[0-9]? with '
        r'magnitude of [2-7]\.?[0-9]?', out, re.I)


def test_mixed(capsys):
    tutorial.print_sentiment('reviews/bladerunner-mixed.txt')
    out, _ = capsys.readouterr()
    assert re.search(r'Sentence \d has a sentiment score of \d', out, re.I)
    assert re.search(
        r'Overall Sentiment: score of -?[0-9]\.?[0-9]? with '
        r'magnitude of [3-6]\.?[0-9]?', out, re.I)
