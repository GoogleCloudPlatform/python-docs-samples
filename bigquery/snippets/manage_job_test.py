# Copyright 2022 Google LLC
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

from google.cloud import bigquery
import pytest

import manage_job_cancel
import manage_job_get


def test_manage_job(capsys: pytest.CaptureFixture[str]) -> None:
    client = bigquery.Client()
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    location = "us"
    job = client.query(sql, location=location)

    manage_job_cancel.cancel_job(client, location=location, job_id=job.job_id)
    out, _ = capsys.readouterr()
    assert f"{job.location}:{job.job_id} cancelled" in out

    manage_job_get.get_job(client, location=location, job_id=job.job_id)
    out, _ = capsys.readouterr()
    assert f"{job.location}:{job.job_id}" in out
    assert "Type: query" in out
