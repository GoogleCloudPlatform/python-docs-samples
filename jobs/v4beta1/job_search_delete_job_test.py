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

from google.api_core.exceptions import NotFound

import pytest

import job_search_create_job
import job_search_delete_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_ID = os.environ["JOB_SEARCH_TENANT_ID"]
COMPANY_ID = os.environ["JOB_SEARCH_COMPANY_ID"]
POST_UNIQUE_ID = "TEST_POST_{}".format(uuid.uuid4())[:20]


@pytest.fixture(scope="module")
def job():
    # create a temporary job
    job_name = job_search_create_job.create_job(
        PROJECT_ID, TENANT_ID, COMPANY_ID, POST_UNIQUE_ID, "www.jobUrl.com"
    )

    # extract company id
    job_id = job_name.split("/")[-1]

    yield job_id

    try:
        job_search_delete_job.delete_job(PROJECT_ID, TENANT_ID, job_id)
    except NotFound as e:
        print("Ignoring NotFound upon cleanup, details: {}".format(e))


def test_delete_job(capsys, job):
    job_search_delete_job.delete_job(PROJECT_ID, TENANT_ID, job)
    out, _ = capsys.readouterr()
    assert "Deleted" in out
