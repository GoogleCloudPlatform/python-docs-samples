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
import job_search_create_job
import job_search_create_tenant
import job_search_delete_company
import job_search_delete_job
import job_search_delete_tenant

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def tenant():
    tenant_ext_unique_id = f"TEST_TENANT_{uuid.uuid4()}"
    # create a temporary tenant
    tenant_name = job_search_create_tenant.create_tenant(
        PROJECT_ID, tenant_ext_unique_id
    )

    # extract company id
    tenant_id = tenant_name.split("/")[-1]

    yield tenant_id

    try:
        job_search_delete_tenant.delete_tenant(PROJECT_ID, tenant_id)
    except NotFound as e:
        print(f"Ignoring NotFound upon cleanup, details: {e}")


@pytest.fixture(scope="module")
def company(tenant):
    company_ext_id = f"COMPANY_EXT_ID_{uuid.uuid4()}"

    # create a temporary company
    company_name = job_search_create_company.create_company(
        PROJECT_ID, tenant, "Test Company Name", company_ext_id
    )

    # extract company id
    company_id = company_name.split("/")[-1]

    yield company_id

    try:
        job_search_delete_company.delete_company(PROJECT_ID, tenant, company_id)
    except NotFound as e:
        print(f"Ignoring NotFound upon cleanup, details: {e}")


@pytest.fixture(scope="module")
def job(tenant, company):
    post_unique_id = f"TEST_POST_{uuid.uuid4().hex}"[:20]
    # create a temporary job
    job_name = job_search_create_job.create_job(
        PROJECT_ID, tenant, company, post_unique_id, "www.jobUrl.com"
    )

    # extract company id
    job_id = job_name.split("/")[-1]

    yield job_id

    try:
        job_search_delete_job.delete_job(PROJECT_ID, tenant, job_id)
    except NotFound as e:
        print(f"Ignoring NotFound upon cleanup, details: {e}")
