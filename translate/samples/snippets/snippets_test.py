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

import pytest

import snippets


def test_detect_language(capsys: pytest.LogCaptureFixture) -> None:
    result = snippets.detect_language("Hæ sæta")
    out, _ = capsys.readouterr()
    assert "is" in result["language"]


def test_list_languages(capsys: pytest.LogCaptureFixture) -> None:
    results = snippets.list_languages()
    out, _ = capsys.readouterr()
    for language in results:
        print("{name} ({language})".format(**language))
    assert "Abkhaz" in results[0]["name"]


def test_list_languages_with_target(capsys: pytest.LogCaptureFixture) -> None:
    results = snippets.list_languages_with_target("is")
    out, _ = capsys.readouterr()
    assert "abkasíska" in results[0]["name"]


def test_translate_text(capsys: pytest.LogCaptureFixture) -> None:
    result = snippets.translate_text(text="Hello world", target_language="is")
    out, _ = capsys.readouterr()
    assert "Halló heimur" in result[0]["translatedText"]


def test_translate_utf8(capsys: pytest.LogCaptureFixture) -> None:
    text = "파인애플 13개"
    result = snippets.translate_text(text=text, target_language="en")
    out, _ = capsys.readouterr()
    assert "13 pineapples" in result[0]["translatedText"]
