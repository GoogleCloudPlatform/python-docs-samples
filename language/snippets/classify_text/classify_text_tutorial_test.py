# Copyright 2016 Google LLC
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

import pytest

import classify_text_tutorial

OUTPUT = "index.json"
RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
QUERY_TEXT = """Google Home enables users to speak voice commands to interact
with services through the Home\'s intelligent personal assistant called
Google Assistant. A large number of services, both in-house and third-party,
are integrated, allowing users to listen to music, look at videos or photos,
or receive news updates entirely by voice."""
QUERY_CATEGORY = "/Computers & Electronics/Software"


@pytest.fixture(scope="session")
def index_file(tmpdir_factory):
    temp_file = tmpdir_factory.mktemp("tmp").join(OUTPUT)
    temp_out = temp_file.strpath
    classify_text_tutorial.index(os.path.join(RESOURCES, "texts"), temp_out)
    return temp_file


def test_classify(capsys):
    with open(os.path.join(RESOURCES, "query_text1.txt")) as f:
        text = f.read()
    classify_text_tutorial.classify(text)
    out, err = capsys.readouterr()
    assert "category" in out


def test_index(capsys, tmpdir):
    temp_dir = tmpdir.mkdir("tmp")
    temp_out = temp_dir.join(OUTPUT).strpath

    classify_text_tutorial.index(os.path.join(RESOURCES, "texts"), temp_out)
    out, err = capsys.readouterr()

    assert OUTPUT in out
    assert len(temp_dir.listdir()) == 1


def test_query_text(capsys, index_file):
    temp_out = index_file.strpath

    classify_text_tutorial.query(temp_out, QUERY_TEXT)
    out, err = capsys.readouterr()

    assert "Filename: cloud_computing.txt" in out


def test_query_category(capsys, index_file):
    temp_out = index_file.strpath

    classify_text_tutorial.query_category(temp_out, QUERY_CATEGORY)
    out, err = capsys.readouterr()

    assert "Filename: cloud_computing.txt" in out


def test_split_labels():
    categories = {"/a/b/c": 1.0}
    split_categories = {"a": 1.0, "b": 1.0, "c": 1.0}
    assert classify_text_tutorial.split_labels(categories) == split_categories


def test_similarity():
    empty_categories = {}
    categories1 = {"/a/b/c": 1.0, "/d/e": 1.0}
    categories2 = {"/a/b": 1.0}

    assert classify_text_tutorial.similarity(empty_categories, categories1) == 0.0
    assert classify_text_tutorial.similarity(categories1, categories1) > 0.99
    assert classify_text_tutorial.similarity(categories1, categories2) > 0
    assert classify_text_tutorial.similarity(categories1, categories2) < 1
