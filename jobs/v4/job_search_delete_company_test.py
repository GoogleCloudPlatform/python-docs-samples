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
import job_search_delete_company
import job_search_create_company

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_ID = "b603d325-3fb5-4979-8994-eba4ecf726f4"
COMPANY_EXT_ID = "COMPANY_EXT_ID_{}".format(uuid.uuid4())


def test_delete_company(capsys):
    # set up
    job_search_create_company.create_company(
        PROJECT_ID, TENANT_ID, "Test Company Name", COMPANY_EXT_ID
    )
    out, _ = capsys.readouterr()

    # extract company id
    company_id = out.splitlines()[1].split()[1].split("/")[-1]

    job_search_delete_company.delete_company(PROJECT_ID, TENANT_ID, company_id)
    out, _ = capsys.readouterr()
    assert "Deleted" in out
