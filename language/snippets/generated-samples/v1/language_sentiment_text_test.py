# Copyright 2018 Google, Inc.
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

import language_sentiment_text


def test_analyze_sentiment_text_positive(capsys):
    language_sentiment_text.sample_analyze_sentiment("Happy Happy Joy Joy")
    out, _ = capsys.readouterr()
    assert "Score: 0." in out


def test_analyze_sentiment_text_negative(capsys):
    language_sentiment_text.sample_analyze_sentiment("Angry Angry Sad Sad")
    out, _ = capsys.readouterr()
    assert "Score: -0." in out
