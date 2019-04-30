# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import mock
import pytest

PROJECT = os.environ['GCLOUD_PROJECT']


@pytest.fixture
def api_client_inject_project_id():
    """Patches all googleapiclient requests to replace 'YOUR_PROJECT_ID' with
    the project ID."""
    import googleapiclient.http

    old_execute = googleapiclient.http.HttpRequest.execute

    def new_execute(self, http=None, num_retries=0):
        self.uri = self.uri.replace('YOUR_PROJECT_ID', PROJECT)
        return old_execute(self, http=http, num_retries=num_retries)

    with mock.patch(
            'googleapiclient.http.HttpRequest.execute',
            new=new_execute):
        yield
