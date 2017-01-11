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

import pytest

import detect


def test_quickstart(capsys):
    detect.run_all_local()
    out, _ = capsys.readouterr()
    assert 'Labels' in out
    assert 'Landmarks' in out
    assert 'Faces' in out
    assert 'Logos' in out
    assert 'Safe search' in out
    # TODO: uncomment when https://goo.gl/c47YwV is fixed.
    # assert 'Text' in out
    assert 'Properties' in out


def test_labels(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect.detect_labels(file_name)
    out, _ = capsys.readouterr()
    assert 'whiskers' in out


def test_labels_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/wakeupcat.jpg'
    detect.detect_labels_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'whiskers' in out


def test_landmarks(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect.detect_landmarks(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_landmarks_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/landmark.jpg'
    detect.detect_landmarks_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_faces(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    detect.detect_faces(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.POSSIBLE' in out


def test_faces_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/face_no_surprise.jpg'
    detect.detect_faces_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.POSSIBLE' in out


def test_logos(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    detect.detect_logos(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_logos_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/logos.png'
    detect.detect_logos_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_safe_search(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect.detect_safe_search(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.VERY_LIKELY' in out


def test_safe_search_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/wakeupcat.jpg'
    detect.detect_safe_search_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'Likelihood.VERY_LIKELY' in out


@pytest.mark.xfail(reason='Client library needs to be more resilient'
                   + 'https://goo.gl/c47YwV')
def test_detect_text(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect.detect_text(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


@pytest.mark.xfail(reason='Client library needs to be more resilient'
                   + 'https://goo.gl/c47YwV')
def test_detect_text_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/text.jpg'
    detect.detect_text_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_properties(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect.detect_properties(file_name)
    out, _ = capsys.readouterr()
    assert 'fraction' in out


def test_detect_properties_cloud_storage(capsys):
    file_name = 'gs://python-docs-samples-tests/vision/landmark.jpg'
    detect.detect_properties_cloud_storage(file_name)
    out, _ = capsys.readouterr()
    assert 'fraction' in out
