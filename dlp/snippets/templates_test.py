# Copyright 2023 Google LLC
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
import uuid

import google.api_core.exceptions
import google.cloud.storage

import templates

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_TEMPLATE_ID = "test-template" + UNIQUE_STRING


def test_create_list_and_delete_template(capsys):
    try:
        templates.create_inspect_template(
            GCLOUD_PROJECT,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            template_id=TEST_TEMPLATE_ID,
        )
    except google.api_core.exceptions.InvalidArgument:
        # Template already exists, perhaps due to a previous interrupted test.
        templates.delete_inspect_template(GCLOUD_PROJECT, TEST_TEMPLATE_ID)

        out, _ = capsys.readouterr()
        assert TEST_TEMPLATE_ID in out

        # Try again and move on.
        templates.create_inspect_template(
            GCLOUD_PROJECT,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            template_id=TEST_TEMPLATE_ID,
        )

    out, _ = capsys.readouterr()
    assert TEST_TEMPLATE_ID in out

    templates.list_inspect_templates(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert TEST_TEMPLATE_ID in out

    templates.delete_inspect_template(GCLOUD_PROJECT, TEST_TEMPLATE_ID)

    out, _ = capsys.readouterr()
    assert TEST_TEMPLATE_ID in out
