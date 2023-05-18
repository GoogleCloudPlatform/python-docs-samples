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

import job_search_create_job_custom_attributes
import job_search_delete_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
JOB_EXT_UNIQUE_ID = f"TEST_JOB_{uuid.uuid4()}"


def test_create_job_with_attributes(capsys, tenant, company, cleaner):
    job_name = job_search_create_job_custom_attributes.create_job(
        PROJECT_ID, tenant, company, JOB_EXT_UNIQUE_ID
    )
    out, _ = capsys.readouterr()
    assert "Created job:" in out

    # extract job id
    job_id = job_name.split("/")[-1]
    cleaner.append(job_id)


@pytest.fixture(scope="module")
def cleaner(tenant):
    jobs = []

    yield jobs

    for job_id in jobs:
        job_search_delete_job.delete_job(PROJECT_ID, tenant, job_id)
