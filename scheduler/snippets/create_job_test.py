# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import create_job

TEST_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_LOCATION = os.getenv("LOCATION_ID", "us-central1")


def test_create_job(capsys):
    create_result = create_job.create_scheduler_job(
        TEST_PROJECT_ID, TEST_LOCATION, "my-service"
    )
    out, _ = capsys.readouterr()
    assert "Created job:" in out

    job_name = create_result.name.split("/")[-1]
    create_job.delete_scheduler_job(TEST_PROJECT_ID, TEST_LOCATION, job_name)

    out, _ = capsys.readouterr()
    assert "Job deleted." in out
