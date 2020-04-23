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
import job_search_create_tenant
import job_search_delete_tenant

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_EXT_UNIQUE_ID = "TEST_TENANT_{}".format(uuid.uuid4())


def test_create_tenant(capsys):
    # create tenant
    job_search_create_tenant.create_tenant(PROJECT_ID, TENANT_EXT_UNIQUE_ID)
    out, _ = capsys.readouterr()
    assert "Created Tenant" in out

    # extract tenant id
    tenant_id = out.splitlines()[1].split(":")[1].split("/")[-1]

    # tear down
    job_search_delete_tenant.delete_tenant(PROJECT_ID, tenant_id)

    out, _ = capsys.readouterr()
    assert "Deleted" in out
