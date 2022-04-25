#!/usr/bin/env python

# Copyright 2019 Google, LLC
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
from urllib.request import urlopen
import uuid

import backoff
from google.api_core.exceptions import Conflict
from google.cloud import storage
import pytest

import beta_snippets

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


@pytest.fixture(scope="session")
def video_path(tmpdir_factory):
    file = urlopen("http://storage.googleapis.com/cloud-samples-data/video/cat.mp4")
    path = tmpdir_factory.mktemp("video").join("file.mp4")
    with open(str(path), "wb") as f:
        f.write(file.read())

    return str(path)


@pytest.fixture(scope="function")
def bucket():
    # Create a temporaty bucket to store annotation output.
    bucket_name = f"tmp-{uuid.uuid4().hex}"
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    # Teardown. We're occasionally seeing 409 conflict errors.
    # Retrying upon 409s.
    @backoff.on_exception(backoff.expo, Conflict, max_time=120)
    def delete_bucket():
        bucket.delete(force=True)

    delete_bucket()


@pytest.mark.slow
def test_speech_transcription(capsys):
    beta_snippets.speech_transcription(
        "gs://python-docs-samples-tests/video/googlework_short.mp4", timeout=240
    )
    out, _ = capsys.readouterr()
    assert "cultural" in out


@pytest.mark.slow
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_labels_streaming(capsys, video_path):
    beta_snippets.detect_labels_streaming(video_path)

    out, _ = capsys.readouterr()
    assert "cat" in out


@pytest.mark.slow
def test_detect_shot_change_streaming(capsys, video_path):
    beta_snippets.detect_shot_change_streaming(video_path)

    out, _ = capsys.readouterr()
    assert "Shot" in out


# Flaky ServiceUnavailable
@pytest.mark.slow
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_track_objects_streaming(capsys, video_path):
    beta_snippets.track_objects_streaming(video_path)

    out, _ = capsys.readouterr()
    assert "cat" in out


@pytest.mark.slow
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_explicit_content_streaming(capsys, video_path):
    beta_snippets.detect_explicit_content_streaming(video_path)

    out, _ = capsys.readouterr()
    assert "Time" in out


@pytest.mark.slow
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_annotation_to_storage_streaming(capsys, video_path, bucket):
    output_uri = "gs://{}".format(bucket.name)
    beta_snippets.annotation_to_storage_streaming(video_path, output_uri)

    out, _ = capsys.readouterr()
    assert "Storage" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_text(capsys):
    in_file = "./resources/googlework_tiny.mp4"
    beta_snippets.video_detect_text(in_file)
    out, _ = capsys.readouterr()
    assert "Text" in out


# Flaky timeout
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_text_gcs(capsys):
    in_file = "gs://python-docs-samples-tests/video/googlework_tiny.mp4"
    beta_snippets.video_detect_text_gcs(in_file)
    out, _ = capsys.readouterr()
    assert "Text" in out


# Flaky Gateway
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_streaming_automl_classification(capsys, video_path):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    model_id = "VCN6363999689846554624"
    beta_snippets.streaming_automl_classification(video_path, project_id, model_id)
    out, _ = capsys.readouterr()
    assert "brush_hair" in out


# Flaky Gateway
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_streaming_automl_object_tracking(capsys, video_path):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    model_id = "VOT282620667826798592"
    beta_snippets.streaming_automl_object_tracking(video_path, project_id, model_id)
    out, _ = capsys.readouterr()
    assert "Track Id" in out


# Flaky Gateway
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_streaming_automl_action_recognition(capsys, video_path):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    model_id = "6597443600609443840"
    beta_snippets.streaming_automl_action_recognition(video_path, project_id, model_id)
    out, _ = capsys.readouterr()
    assert "segment" in out
