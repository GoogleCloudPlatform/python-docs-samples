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

from google.cloud import talent
import pytest

import job_search_list_tenants

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def test_tenant():
    client = talent.TenantServiceClient()
    external_id = f"test_tenant_{uuid.uuid4().hex}"
    parent = f"projects/{PROJECT_ID}"
    tenant = {"external_id": external_id}
    resp = client.create_tenant(parent=parent, tenant=tenant)

    yield resp

    client.delete_tenant(name=resp.name)


def test_list_tenants(capsys, test_tenant):
    job_search_list_tenants.list_tenants(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "Tenant Name:" in out
