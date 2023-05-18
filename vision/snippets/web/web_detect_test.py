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

import pytest

import web_detect

ASSET_BUCKET = "cloud-samples-data"


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_file(capsys):
    file_name = ('../detect/resources/landmark.jpg')
    web_detect.report(web_detect.annotate(file_name))
    out, _ = capsys.readouterr()
    assert 'description' in out.lower()


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_detect_web_gsuri(capsys):
    file_name = ('gs://{}/vision/landmark/pofa.jpg'.format(
                 ASSET_BUCKET))
    web_detect.report(web_detect.annotate(file_name))
    out, _ = capsys.readouterr()
    assert 'description:' in out.lower()
