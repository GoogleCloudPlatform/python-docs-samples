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

from classify_text_tutorial import classify
from classify_text_tutorial import similarity
from classify_text_tutorial import split_labels

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_classify(capsys):
    with open(os.path.join(RESOURCES, 'query_text1.txt'), 'r') as f:
        text = f.read()
    classify(text)
    out, err = capsys.readouterr()
    assert 'category' in out


def test_split_labels():
    categories = {'/a/b/c': 1.0}
    split_categories = {'a': 1.0, 'b': 1.0, 'c': 1.0}
    assert split_labels(categories) == split_categories


def test_similarity():
    empty_categories = {}
    categories1 = {'/a/b/c': 1.0, '/d/e': 1.0}
    categories2 = {'/a/b': 1.0}

    assert similarity(empty_categories, categories1) == 0.0
    assert similarity(categories1, categories1) > 0.99
    assert similarity(categories1, categories2) > 0
    assert similarity(categories1, categories2) < 1
