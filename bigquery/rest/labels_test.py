# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from labels import label_dataset, label_table

PROJECT = os.environ['GCLOUD_PROJECT']


def test_label_dataset(capsys):
    label_dataset(
        'test_dataset',
        'environment',
        'test',
        project_id=PROJECT)

    out, _ = capsys.readouterr()
    result = out.split('\n')[0]

    assert 'Updated label "environment" with value "test"' in result


def test_label_table(capsys):
    label_table(
        'test_dataset',
        'test_table',
        'data-owner',
        'my-team',
        project_id=PROJECT)

    out, _ = capsys.readouterr()
    result = out.split('\n')[0]

    assert 'Updated label "data-owner" with value "my-team"' in result
