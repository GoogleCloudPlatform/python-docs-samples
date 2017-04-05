# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

import main

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_dependents():
    text = "I am eating a delicious banana"
    analysis = main.analyze_syntax(text)
    tokens = analysis.get('tokens', [])
    assert [0, 1, 5] == main.dependents(tokens, 2)
    assert [3, 4] == main.dependents(tokens, 5)


def test_phrase_text_for_head():
    text = "A small collection of words"
    analysis = main.analyze_syntax(text)
    tokens = analysis.get('tokens', [])
    assert "words" == main.phrase_text_for_head(tokens, text, 4)


def test_find_triples():
    text = "President Obama won the noble prize"
    analysis = main.analyze_syntax(text)
    tokens = analysis.get('tokens', [])
    triples = main.find_triples(tokens)
    for triple in triples:
        assert (1, 2, 5) == triple


def test_obama_example(capsys):
    main.main(os.path.join(RESOURCES, 'obama_wikipedia.txt'))
    stdout, _ = capsys.readouterr()
    lines = stdout.split('\n')
    assert re.match(
        r'.*Obama\b.*\| received\b.*\| national attention\b',
        lines[1])
