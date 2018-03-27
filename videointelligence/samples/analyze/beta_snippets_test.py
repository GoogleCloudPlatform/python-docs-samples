#!/usr/bin/env python

# Copyright 2017 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

import beta_snippets


BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
FACES_SHORT_FILE_PATH = 'video/googlework_short.mp4'


@pytest.mark.slow
def test_face_bounding_boxes(capsys):
    beta_snippets.face_bounding_boxes(
        'gs://{}/{}'.format(BUCKET, FACES_SHORT_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'top   :' in out


@pytest.mark.slow
def test_face_emotions(capsys):
    beta_snippets.face_emotions(
        'gs://{}/{}'.format(BUCKET, FACES_SHORT_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'CONCENTRATION' in out


@pytest.mark.slow
def test_speech_transcription(capsys):
    beta_snippets.speech_transcription(
        'gs://{}/{}'.format(BUCKET, FACES_SHORT_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'cultural' in out
