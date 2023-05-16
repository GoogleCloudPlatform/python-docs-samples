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

import job_search_create_company
import job_search_delete_company

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
COMPANY_EXT_ID = f"COMPANY_EXT_ID_{uuid.uuid4()}"


def test_create_company(capsys, tenant, cleaner):
    # create company
    company_name = job_search_create_company.create_company(
        PROJECT_ID, tenant, "Test Company Name", COMPANY_EXT_ID
    )
    out, _ = capsys.readouterr()
    assert "Created" in out
    assert "Name:" in out

    # extract id
    company_id = company_name.split("/")[-1]
    cleaner.append(company_id)


@pytest.fixture(scope="module")
def cleaner(tenant):
    companies = []

    yield companies

    for company_id in companies:
        job_search_delete_company.delete_company(PROJECT_ID, tenant, company_id)
