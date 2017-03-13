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


LABELS_FILE_PATH = '/video/cat.mp4'
FACES_FILE_PATH = '/video/gbike.mp4'
SHOTS_FILE_PATH = '/video/gbikes_dinosaur.mp4'


@pytest.mark.slow
def test_cat_video_shots(capsys, cloud_config):
    analyze.analyze_shots(
        'gs://{}{}'.format(cloud_config.storage_bucket, SHOTS_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Scene 1:' in out


@pytest.mark.slow
def test_cat_video_faces(capsys, cloud_config):
    analyze.analyze_faces(
        'gs://{}{}'.format(cloud_config.storage_bucket, FACES_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Thumbnail' in out


@pytest.mark.slow
def test_cat_video_labels(capsys, cloud_config):
    analyze.analyze_labels(
        'gs://{}{}'.format(cloud_config.storage_bucket, LABELS_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Whiskers' in out
