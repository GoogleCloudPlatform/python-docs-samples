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

import analyze

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
LABELS_FILE_PATH = '/video/cat.mp4'
FACES_FILE_PATH = '/video/googlework.mp4'
SHOTS_FILE_PATH = '/video/gbikes_dinosaur.mp4'


@pytest.mark.slow
def test_cat_video_shots(capsys):
    analyze.analyze_shots(
        'gs://{}{}'.format(BUCKET, SHOTS_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Scene 1:' in out


@pytest.mark.slow
def test_work_video_faces(capsys):
    analyze.analyze_faces(
        'gs://{}{}'.format(BUCKET, FACES_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Thumbnail' in out


@pytest.mark.slow
def test_dino_video_labels(capsys):
    analyze.analyze_labels(
        'gs://{}{}'.format(BUCKET, LABELS_FILE_PATH))
    out, _ = capsys.readouterr()
    assert 'Whiskers' in out
