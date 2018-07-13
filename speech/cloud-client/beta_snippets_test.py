# Copyright 2018, Google, Inc.
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

from beta_snippets import (
    transcribe_file_with_auto_punctuation,
    transcribe_file_with_diarization,
    transcribe_file_with_enhanced_model,
    transcribe_file_with_metadata,
    transcribe_file_with_multichannel,
    transcribe_file_with_multilanguage)

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_transcribe_file_with_enhanced_model(capsys):
    transcribe_file_with_enhanced_model(
        os.path.join(RESOURCES, 'commercial_mono.wav'))
    out, _ = capsys.readouterr()

    assert 'Chrome' in out


def test_transcribe_file_with_metadata(capsys):
    transcribe_file_with_metadata(
        os.path.join(RESOURCES, 'commercial_mono.wav'))
    out, _ = capsys.readouterr()

    assert 'Chrome' in out


def test_transcribe_file_with_auto_punctuation(capsys):
    transcribe_file_with_auto_punctuation(
        os.path.join(RESOURCES, 'commercial_mono.wav'))
    out, _ = capsys.readouterr()

    assert 'Okay. Sure.' in out


def test_transcribe_diarization(capsys):
    transcribe_file_with_diarization(
        os.path.join(RESOURCES, 'Google_Gnome.wav'))
    out, err = capsys.readouterr()

    assert 'OK Google stream stranger things from Netflix to my TV' in out


def test_transcribe_multichannel_file(capsys):
    transcribe_file_with_multichannel(
        os.path.join(RESOURCES, 'Google_Gnome.wav'))
    out, err = capsys.readouterr()

    assert 'OK Google stream stranger things from Netflix to my TV' in out


def test_transcribe_multilanguage_file(capsys):
    transcribe_file_with_multilanguage(
        os.path.join(RESOURCES, 'multi.wav'), 'en-US', 'es')
    out, err = capsys.readouterr()

    assert 'how are you doing estoy bien e tu' in out
