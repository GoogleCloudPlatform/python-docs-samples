#!/usr/bin/env python

# Copyright 2017 Google LLC
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

import time

from google.api_core.exceptions import ServiceUnavailable
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


def test_analyze_shots(capsys):
    analyze.analyze_shots("gs://cloud-samples-data/video/gbikes_dinosaur.mp4")
    out, _ = capsys.readouterr()
    assert "Shot 1:" in out


def test_analyze_labels(capsys):
    analyze.analyze_labels("gs://cloud-samples-data/video/cat.mp4")
    out, _ = capsys.readouterr()
    assert "label description: cat" in out


def test_analyze_labels_file(capsys):
    analyze.analyze_labels_file("resources/googlework_tiny.mp4")
    out, _ = capsys.readouterr()
    assert "label description" in out


def test_analyze_explicit_content(capsys):
    try_count = 0
    while try_count < 3:
        try:
            analyze.analyze_explicit_content("gs://cloud-samples-data/video/cat.mp4")
            out, _ = capsys.readouterr()
            assert "pornography" in out
        except ServiceUnavailable as e:
            # Service is throttling or not available for the moment, sleep for 5 sec and retrying again.
            print("Got service unavailable exception: {}".format(str(e)))
            time.sleep(5)
            continue
        try_count = try_count + 1
        break


def test_speech_transcription(capsys):
    analyze.speech_transcription("gs://cloud-samples-data/video/googlework_short.mp4")
    out, _ = capsys.readouterr()
    assert "cultural" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_text_gcs(capsys):
    analyze.video_detect_text_gcs("gs://cloud-samples-data/video/googlework_tiny.mp4")
    out, _ = capsys.readouterr()
    assert "Text" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_text(capsys):
    analyze.video_detect_text("resources/googlework_tiny.mp4")
    out, _ = capsys.readouterr()
    assert "Text" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_track_objects_gcs(capsys):
    analyze.track_objects_gcs("gs://cloud-samples-data/video/cat.mp4")
    out, _ = capsys.readouterr()
    assert "cat" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_track_objects(capsys):
    in_file = "./resources/googlework_tiny.mp4"
    analyze.track_objects(in_file)
    out, _ = capsys.readouterr()
    assert "Entity id" in out
