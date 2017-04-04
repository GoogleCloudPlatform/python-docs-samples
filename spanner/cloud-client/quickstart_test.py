# Copyright 2016 Google Inc. All Rights Reserved.
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

from google.cloud import spanner
import google.cloud.exceptions
import google.cloud.spanner.client
import mock
import pytest

import quickstart

SPANNER_INSTANCE = os.environ['SPANNER_INSTANCE']


@pytest.fixture
def patch_instance():
    original_instance = google.cloud.spanner.client.Client.instance

    def new_instance(self, unused_instance_name):
        return original_instance(self, SPANNER_INSTANCE)

    instance_patch = mock.patch(
        'google.cloud.spanner.client.Client.instance',
        side_effect=new_instance,
        autospec=True)

    with instance_patch:
        yield


@pytest.fixture
def example_database():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(SPANNER_INSTANCE)
    database = instance.database('my-database-id')

    if not database.exists():
        database.create()

    yield


def test_quickstart(capsys, patch_instance, example_database):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert '[1]' in out
