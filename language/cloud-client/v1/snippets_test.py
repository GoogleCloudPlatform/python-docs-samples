# -*- coding: utf-8 -*-
# Copyright 2018 Google, LLC.
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

import snippets


def test_sentiment_text(capsys):
    snippets.sentiment_text()
    out, _ = capsys.readouterr()
    assert 'Score: ' in out


def test_sentiment_file(capsys):
    snippets.sentiment_file()
    out, _ = capsys.readouterr()
    assert 'Score: ' in out


def test_entities_text(capsys):
    snippets.entities_text()
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert ': Kennedy' in out


def test_entities_file(capsys):
    snippets.entities_file()
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert ': Kennedy' in out


def test_syntax_text(capsys):
    snippets.syntax_text()
    out, _ = capsys.readouterr()
    assert 'NOUN: President' in out


def test_syntax_file(capsys):
    snippets.syntax_file()
    out, _ = capsys.readouterr()
    assert 'NOUN: President' in out


def test_sentiment_entities_text(capsys):
    snippets.entity_sentiment_text()
    out, _ = capsys.readouterr()
    assert 'Content : White House' in out


def test_sentiment_entities_file(capsys):
    snippets.entity_sentiment_file()
    out, _ = capsys.readouterr()
    assert 'Content : White House' in out


def test_classify_text(capsys):
    snippets.classify_text()
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert '/Computers & Electronics' in out


def test_classify_file(capsys):
    snippets.classify_file()
    out, _ = capsys.readouterr()
    assert 'name' in out
    assert '/Computers & Electronics' in out
