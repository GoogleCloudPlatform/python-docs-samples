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

import job_search_create_tenant
import job_search_delete_tenant

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_EXT_UNIQUE_ID = f"TEST_TENANT_{uuid.uuid4()}"


def test_create_tenant(capsys, cleaner):
    # create tenant
    tenant_name = job_search_create_tenant.create_tenant(
        PROJECT_ID, TENANT_EXT_UNIQUE_ID
    )
    out, _ = capsys.readouterr()
    assert "Created Tenant" in out
    assert "Name:" in out

    # extract tenant id
    tenant_id = tenant_name.split("/")[-1]
    cleaner.append(tenant_id)


@pytest.fixture(scope="module")
def cleaner():
    tenants = []

    yield tenants

    for tenant_id in tenants:
        job_search_delete_tenant.delete_tenant(PROJECT_ID, tenant_id)
