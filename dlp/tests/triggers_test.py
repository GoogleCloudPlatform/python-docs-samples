# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.api_core.exceptions
import google.cloud.storage
import pytest

import dlp.triggers as triggers
from dlp.tests.test_utils import bucket, vpc_check

GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_BUCKET_NAME = GCLOUD_PROJECT + '-dlp-python-client-test'
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCE_FILE_NAMES = ['test.txt', 'test.png', 'harmless.txt', 'accounts.txt']
TEST_TRIGGER_ID = 'test-trigger'


@vpc_check
@pytest.mark.usefixtures("bucket")
def test_create_list_and_delete_trigger(bucket, capsys):
    try:
        triggers.create_trigger(
            GCLOUD_PROJECT, bucket.name, 7,
            ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'],
            trigger_id=TEST_TRIGGER_ID,
        )
    except google.api_core.exceptions.InvalidArgument:
        # Trigger already exists, perhaps due to a previous interrupted test.
        triggers.delete_trigger(GCLOUD_PROJECT, TEST_TRIGGER_ID)

        out, _ = capsys.readouterr()
        assert TEST_TRIGGER_ID in out

        # Try again and move on.
        triggers.create_trigger(
            GCLOUD_PROJECT, bucket.name, 7,
            ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'],
            trigger_id=TEST_TRIGGER_ID,
            auto_populate_timespan=True,
        )

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out

    triggers.list_triggers(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out

    triggers.delete_trigger(GCLOUD_PROJECT, TEST_TRIGGER_ID)

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out
