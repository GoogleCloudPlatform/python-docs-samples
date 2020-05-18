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

import job_search_create_company
import job_search_delete_company

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_ID = os.environ["JOB_SEARCH_TENANT_ID"]
COMPANY_EXT_ID = "COMPANY_EXT_ID_{}".format(uuid.uuid4())


@pytest.fixture(scope="module")
def company():
    # create a temporary company
    company_name = job_search_create_company.create_company(
        PROJECT_ID, TENANT_ID, "Test Company Name", COMPANY_EXT_ID
    )

    # extract company id
    company_id = company_name.split("/")[-1]

    yield company_id

<<<<<<< HEAD
=======
    try:
        job_search_delete_company.delete_company(PROJECT_ID, TENANT_ID, company)
    except NotFound as e:
        print("Ignoring NotFound upon cleanup, details: {}".format(e))

>>>>>>> e454c4e2bb70245a74b2fa54984f9bc98beea43a

def test_delete_company(capsys, company):
    out, _ = capsys.readouterr()

    job_search_delete_company.delete_company(PROJECT_ID, TENANT_ID, company)
    out, _ = capsys.readouterr()
    assert "Deleted" in out
