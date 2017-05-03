# Copyright 2017 Google Inc.
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

import google.auth
import mock
import pytest

from user_credentials import authenticate_and_query


PROJECT = os.environ['GCLOUD_PROJECT']


@pytest.fixture
def mock_flow():
    flow_patch = mock.patch(
        'google_auth_oauthlib.flow.InstalledAppFlow', autospec=True)

    with flow_patch as flow_mock:
        flow_mock.from_client_secrets_file.return_value = flow_mock
        flow_mock.credentials = google.auth.default()[0]
        yield flow_mock


def test_auth_query_console(mock_flow, capsys):
    authenticate_and_query(PROJECT, 'SELECT 1+1;', launch_browser=False)
    out, _ = capsys.readouterr()
    assert '2' in out
