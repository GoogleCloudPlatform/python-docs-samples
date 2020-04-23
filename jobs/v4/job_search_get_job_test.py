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
import job_search_get_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_ID = "b603d325-3fb5-4979-8994-eba4ecf726f4"
JOB_ID = "126864868218151622"


def test_job_search_get_job(capsys):
    job_search_get_job.get_job(PROJECT_ID, TENANT_ID, JOB_ID)
    out, _ = capsys.readouterr()
    assert "Job name:" in out
