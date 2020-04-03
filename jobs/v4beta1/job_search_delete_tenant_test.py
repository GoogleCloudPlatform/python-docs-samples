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
TENANT_EXT_UNIQUE_ID = "TEST_TENANT_{}".format(uuid.uuid4())


@pytest.fixture(scope="module")
def tenant():
    # create a temporary company
    tenant_name = job_search_create_tenant.create_tenant(
        PROJECT_ID, TENANT_EXT_UNIQUE_ID
    )

    # extract company id
    tenant_id = tenant_name.split("/")[-1]

    yield tenant_id


def test_delete_tenant(capsys, tenant):
    job_search_delete_tenant.delete_tenant(PROJECT_ID, tenant)
    out, _ = capsys.readouterr()
    assert "Deleted" in out
