# Copyright 2016 Google, Inc.
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


def test_detect_language(capsys):
    snippets.detect_language("Hæ sæta")
    out, _ = capsys.readouterr()
    assert "is" in out


def test_list_languages(capsys):
    snippets.list_languages()
    out, _ = capsys.readouterr()
    assert "Icelandic (is)" in out


def test_list_languages_with_target(capsys):
    snippets.list_languages_with_target("is")
    out, _ = capsys.readouterr()
    assert "íslenska (is)" in out


def test_translate_text(capsys):
    snippets.translate_text("is", "Hello world")
    out, _ = capsys.readouterr()
    assert "Halló heimur" in out


def test_translate_utf8(capsys):
    text = "파인애플 13개"
    snippets.translate_text("en", text)
    out, _ = capsys.readouterr()
    assert "13 pineapples" in out
