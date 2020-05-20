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

import job_search_delete_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_delete_job(capsys, tenant, job):
    job_search_delete_job.delete_job(PROJECT_ID, tenant, job)
    out, _ = capsys.readouterr()
    assert "Deleted" in out
