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

from beta_snippets import (
    detect_document,
    detect_safe_search,
    detect_web,
    web_entities,
    web_entities_include_geo_results,
    web_entities_include_geo_results_uri
)

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


def test_file_with_geo(capsys):
    path = 'resources/city.jpg'
    web_entities_include_geo_results(path)
    out, _ = capsys.readouterr()

    assert 'Zepra' in out


def test_gcsuri_with_geo(capsys):
    uri = 'gs://{}/vision/landmark.jpg'.format(BUCKET)
    web_entities_include_geo_results_uri(uri)
    out, _ = capsys.readouterr()

    assert 'Description: Palace of Fine Arts Theatre' in out


def test_file_without_geo(capsys):
    path = 'resources/city.jpg'
    web_entities(path)
    out, _ = capsys.readouterr()

    assert 'Zepra' not in out


def test_detect_document_path(capsys):
    path = 'resources/text.jpg'
    detect_document(path)
    out, _ = capsys.readouterr()

    assert 'Word text: class (confidence:' in out


def test_safe_search(capsys):
    path = 'resources/wakeupcat.jpg'
    detect_safe_search(path)
    out, _ = capsys.readouterr()

    assert 'VERY_LIKELY' in out
    assert 'racy: ' in out


def test_detect_file(capsys):
    path = 'resources/landmark.jpg'
    detect_web(path)
    out, _ = capsys.readouterr()

    assert 'Description: Palace of Fine Arts Theatre' in out
    assert 'Best guess label: palace of fine arts' in out
