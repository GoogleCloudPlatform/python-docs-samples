# Copyright 2017 Google Inc. All Rights Reserved.
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

import snippets


def test_quickstart(capsys):
    snippets.run_snippets()
    out, _ = capsys.readouterr()
    assert 'Labels' in out
    assert 'Landmarks' in out
    assert 'Faces' in out
    assert 'Logos' in out
    assert 'Safe search' in out
    assert 'Text' in out
    assert 'Properties' in out


def test_labels(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    snippets.detect_labels(file_name)
    out, _ = capsys.readouterr()
    assert 'whiskers' in out


def test_labels_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/wakeupcat.jpg'
    snippets.detect_labels_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'whiskers' in out


def test_landmarks(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    snippets.detect_landmarks(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_landmarks_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/landmark.jpg'
    snippets.detect_landmarks_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_faces(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    snippets.detect_faces(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.POSSIBLE' in out


def test_faces_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/face_no_surprise.jpg'
    snippets.detect_faces_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.POSSIBLE' in out


def test_logos(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    snippets.detect_logos(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_logos_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/logos.png'
    snippets.detect_logos_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_safe_search(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    snippets.detect_safe_search(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.VERY_LIKELY' in out


def test_safe_search_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/wakeupcat.jpg'
    snippets.detect_safe_search_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.VERY_LIKELY' in out


def test_detect_text(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    snippets.detect_text(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_text_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/text.jpg'
    snippets.detect_text_gcs(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_properties(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    snippets.detect_properties(file_name)
    out, _ = capsys.readouterr()
    assert 'fraction' in out


def test_detect_properties_gcs(capsys):
    file_name = 'gs://cloud-samples-tests/vision/landmark.jpg'
    snippets.detect_properties_gcs(file_name)
    out, _ = capsys.readouterr()
    assert 'fraction' in out
