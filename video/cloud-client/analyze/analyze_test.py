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

import analyze

POSSIBLE_TEXTS = [
    "Google",
    "SUR",
    "SUR",
    "ROTO",
    "Vice President",
    "58oo9",
    "LONDRES",
    "OMAR",
    "PARIS",
    "METRO",
    "RUE",
    "CARLO",
]


@pytest.mark.slow
def test_analyze_shots(capsys):
    analyze.analyze_shots("gs://cloud-samples-data/video/gbikes_dinosaur.mp4")
    out, _ = capsys.readouterr()
    assert "Shot 1:" in out


@pytest.mark.slow
def test_analyze_labels(capsys):
    analyze.analyze_labels("gs://cloud-samples-data/video/cat.mp4")
    out, _ = capsys.readouterr()
    assert "label description: cat" in out


@pytest.mark.slow
def test_analyze_labels_file(capsys):
    analyze.analyze_labels_file("resources/googlework_tiny.mp4")
    out, _ = capsys.readouterr()
    assert "label description" in out


@pytest.mark.slow
def test_analyze_explicit_content(capsys):
    analyze.analyze_explicit_content("gs://cloud-samples-data/video/cat.mp4")
    out, _ = capsys.readouterr()
    assert "pornography" in out


@pytest.mark.slow
def test_speech_transcription(capsys):
    analyze.speech_transcription("gs://cloud-samples-data/video/googlework_short.mp4")
    out, _ = capsys.readouterr()
    assert "cultural" in out


@pytest.mark.slow
def test_detect_text_gcs(capsys):
    analyze.video_detect_text_gcs("gs://cloud-samples-data/video/googlework_tiny.mp4")
    out, _ = capsys.readouterr()

    text_exists = False
    out_upper = out.upper()
    for possible_text in POSSIBLE_TEXTS:
        if possible_text.upper() in out_upper:
            text_exists = True
    assert text_exists


@pytest.mark.slow
def test_detect_text(capsys):
    analyze.video_detect_text("resources/googlework_tiny.mp4")
    out, _ = capsys.readouterr()
    assert 'Text' in out


@pytest.mark.slow
def test_track_objects_gcs(capsys):
    analyze.track_objects_gcs("gs://cloud-samples-data/video/cat.mp4")
    out, _ = capsys.readouterr()
    assert "cat" in out


@pytest.mark.slow
def test_track_objects(capsys):
    in_file = "./resources/googlework_tiny.mp4"
    analyze.track_objects(in_file)
    out, _ = capsys.readouterr()
    assert "Entity id" in out
