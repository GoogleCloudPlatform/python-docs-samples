#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import language_sentiment_text


def test_sample_analyze_sentiment_text(capsys: ...) -> None:
    assert os.environ["GOOGLE_CLOUD_PROJECT"] != ""

    language_sentiment_text.sample_analyze_sentiment()
    captured = capsys.readouterr()
    assert "Document sentiment score: " in captured.out
    assert "Document sentiment magnitude: " in captured.out
    assert "Sentence text: " in captured.out
    assert "Sentence sentiment score: " in captured.out
    assert "Sentence sentiment magnitude: " in captured.out
    assert "Language of the text: " in captured.out
