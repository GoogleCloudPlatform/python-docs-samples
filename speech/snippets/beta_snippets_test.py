# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from beta_snippets import (
    transcribe_file_with_auto_punctuation,
    transcribe_file_with_diarization,
    transcribe_file_with_enhanced_model,
    transcribe_file_with_metadata,
    transcribe_file_with_multichannel,
    transcribe_file_with_multilanguage,
    transcribe_file_with_spoken_punctuation_end_emojis,
    transcribe_file_with_word_level_confidence,
)

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


def test_transcribe_file_with_enhanced_model(capsys):
    transcribe_file_with_enhanced_model()
    out, _ = capsys.readouterr()

    assert "Chrome" in out


def test_transcribe_file_with_metadata(capsys):
    transcribe_file_with_metadata()
    out, _ = capsys.readouterr()

    assert "Chrome" in out


def test_transcribe_file_with_auto_punctuation(capsys):
    transcribe_file_with_auto_punctuation()
    out, _ = capsys.readouterr()

    assert "First alternative of result " in out


def test_transcribe_diarization(capsys):
    transcribe_file_with_diarization()
    out, err = capsys.readouterr()

    assert "word:" in out
    assert "speaker_tag:" in out


def test_transcribe_multichannel_file(capsys):
    transcribe_file_with_multichannel()
    out, err = capsys.readouterr()

    assert "OK Google stream stranger things from Netflix to my TV" in out


def test_transcribe_multilanguage_file(capsys):
    transcribe_file_with_multilanguage()
    out, err = capsys.readouterr()

    assert "First alternative of result" in out
    assert "Transcript" in out


def test_transcribe_word_level_confidence(capsys):
    transcribe_file_with_word_level_confidence()
    out, err = capsys.readouterr()

    assert "OK Google stream stranger things from Netflix to my TV" in out


def test_transcribe_file_with_spoken_punctuation_end_emojis(capsys):
    transcribe_file_with_spoken_punctuation_end_emojis()
    out, err = capsys.readouterr()

    assert "First alternative of result " in out
