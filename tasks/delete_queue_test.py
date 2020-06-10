# Copyright 2020 Google LLC
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
import uuid
import pytest

import create_queue
import delete_queue


TEST_PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
TEST_LOCATION = os.getenv('TEST_QUEUE_LOCATION', 'us-central1')


@pytest.fixture
def queue_name():
    queue_name = 'test-queue-{}'.format(uuid.uuid4().hex)
    create_queue.create_queue(
        TEST_PROJECT_ID, queue_name, TEST_LOCATION
    )
    return queue_name


def test_delete_queue(capsys, queue_name):
    delete_queue.delete_queue(
        TEST_PROJECT_ID, queue_name, TEST_LOCATION
    )
    out, _ = capsys.readouterr()
    assert 'Deleted queue' in out
