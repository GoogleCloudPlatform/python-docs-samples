# Copyright 2016 Google, Inc.
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

from concurrent.futures import TimeoutError
import os

import backoff
from google.api_core.exceptions import RetryError
import pytest

import admin


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]


class TestDatastoreAdminSnippets:
    def test_client_create(self):
        assert admin.client_create()

    def test_get_index(self):
        indexes = admin.list_indexes(PROJECT)
        if not indexes:
            pytest.skip(
                "Skipping datastore test. At least "
                "one index should present in database."
            )

        assert admin.get_index(PROJECT, indexes[0].index_id)

    def test_list_index(self):
        assert admin.list_indexes(PROJECT)

    @pytest.mark.flaky
    @backoff.on_exception(backoff.expo, (RetryError, TimeoutError), max_tries=3)
    def test_export_import_entities(self):
        response = admin.export_entities(PROJECT, "gs://" + BUCKET)
        assert response

        assert admin.import_entities(PROJECT, response.output_url)
