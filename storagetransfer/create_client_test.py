# Copyright 2021 Google LLC

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

import json

import backoff
from google.api_core.exceptions import RetryError
from googleapiclient.errors import HttpError
import pytest

import create_client
import create_client_apiary


@pytest.fixture()
def job_filter(project_id: str):
    yield json.dumps({'project_id': project_id})


@backoff.on_exception(backoff.expo, (RetryError,), max_time=60)
def test_create_client(job_filter: str):
    client = create_client.create_transfer_client()

    # a simple test to prove a usable client has been created.
    # The output isn't relevant - just that a valid API call can be made.
    # We expect an error to be raised if this operation fails.
    client.list_transfer_jobs({'filter': job_filter, 'page_size': 1})


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_create_client_apiary(job_filter: str):
    client = create_client_apiary.create_transfer_client()

    # a simple test to prove a usable client has been created.
    # The output isn't relevant - just that a valid API call can be made.
    # We expect an error to be raised if this operation fails.
    client.transferJobs().list(
        filter=job_filter,
        pageSize=1).execute()
