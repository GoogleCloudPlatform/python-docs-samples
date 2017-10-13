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

import web_entities


def test_detect_file_with_geo(capsys):
    file_name = ('../detect/resources/city.jpg')
    web_entities.annotate_web_entities(file_name, True)
    out, _ = capsys.readouterr()
    assert 'Zepra' in out


def test_detect_file_without_geo(capsys):
    file_name = ('../detect/resources/city.jpg')
    web_entities.annotate_web_entities(file_name, False)
    out, _ = capsys.readouterr()
    assert 'Zepra' not in out
