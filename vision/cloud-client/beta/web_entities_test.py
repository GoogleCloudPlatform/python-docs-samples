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

from web_entities import web_entities_file
from web_entities_include_geo_results import (
    web_entities_include_geo_results_file,
    web_entities_include_geo_results_uri)

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


def test_file_with_geo(capsys):
    image_file_path = ('resources/city.jpg')
    web_entities_include_geo_results_file(image_file_path)
    out, _ = capsys.readouterr()

    assert 'Zepra' in out


def test_gcsuri_with_geo(capsys):
    image_uri = ('gs://{}/vision/landmark.jpg'.format(
                 BUCKET))
    web_entities_include_geo_results_uri(image_uri)
    out, _ = capsys.readouterr()

    assert 'Description: Palace of Fine Arts Theatre' in out


def test_file_without_geo(capsys):
    image_file_path = ('resources/city.jpg')
    web_entities_file(image_file_path)
    out, _ = capsys.readouterr()

    assert 'Zepra' not in out
