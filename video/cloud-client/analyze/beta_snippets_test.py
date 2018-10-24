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

import pytest

import beta_snippets

POSSIBLE_TEXTS = ['Google', 'SUR', 'SUR', 'ROTO', 'Vice President', '58oo9',
                  'LONDRES', 'OMAR', 'PARIS', 'METRO', 'RUE', 'CARLO']


@pytest.mark.slow
def test_speech_transcription(capsys):
    beta_snippets.speech_transcription(
        'gs://python-docs-samples-tests/video/googlework_short.mp4')
    out, _ = capsys.readouterr()
    assert 'cultural' in out


@pytest.mark.slow
def test_detect_text():
    in_file = './resources/googlework_short.mp4'
    text_annotations = beta_snippets.video_detect_text(in_file)

    text_exists = False
    for text_annotation in text_annotations:
        for possible_text in POSSIBLE_TEXTS:
            if possible_text.upper() in text_annotation.text.upper():
                text_exists = True
    assert text_exists


@pytest.mark.slow
def test_detect_text_gcs():
    in_file = 'gs://python-docs-samples-tests/video/googlework_short.mp4'
    text_annotations = beta_snippets.video_detect_text_gcs(in_file)

    text_exists = False
    for text_annotation in text_annotations:
        for possible_text in POSSIBLE_TEXTS:
            if possible_text.upper() in text_annotation.text.upper():
                text_exists = True
    assert text_exists


@pytest.mark.slow
def test_track_objects():
    in_file = './resources/cat.mp4'
    object_annotations = beta_snippets.track_objects(in_file)

    text_exists = False
    for object_annotation in object_annotations:
        if 'CAT' in object_annotation.entity.description.upper():
            text_exists = True
    assert text_exists
    assert object_annotations[0].frames[0].normalized_bounding_box.left >= 0.0
    assert object_annotations[0].frames[0].normalized_bounding_box.left <= 1.0


@pytest.mark.slow
def test_track_objects_gcs():
    in_file = 'gs://demomaker/cat.mp4'
    object_annotations = beta_snippets.track_objects_gcs(in_file)

    text_exists = False
    for object_annotation in object_annotations:
        if 'CAT' in object_annotation.entity.description.upper():
            text_exists = True
    assert text_exists
    assert object_annotations[0].frames[0].normalized_bounding_box.left >= 0.0
    assert object_annotations[0].frames[0].normalized_bounding_box.left <= 1.0
