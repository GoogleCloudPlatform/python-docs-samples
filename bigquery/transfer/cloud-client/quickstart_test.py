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

import os

import mock
import pytest

import quickstart


PROJECT = os.environ['GCLOUD_PROJECT']


@pytest.fixture
def mock_project_path():
    """Mock out project and replace with project from environment."""
    project_patch = mock.patch(
        'google.cloud.bigquery_datatransfer.DataTransferServiceClient.'
        'project_path')

    with project_patch as project_mock:
        project_mock.return_value = 'projects/{}'.format(PROJECT)
        yield project_mock


def test_quickstart(capsys, mock_project_path):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert 'Supported Data Sources:' in out
