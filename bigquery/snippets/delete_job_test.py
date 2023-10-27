# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from google.cloud import bigquery

import delete_job  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_delete_job_metadata(
    capsys: "pytest.CaptureFixture[str]",
    bigquery_client: bigquery.Client,
    table_id_us_east1: str,
) -> None:
    query_job: bigquery.QueryJob = bigquery_client.query(
        f"SELECT COUNT(*) FROM `{table_id_us_east1}`",
        location="us-east1",
    )
    query_job.result()
    assert query_job.job_id is not None

    delete_job.delete_job_metadata(query_job.job_id, "us-east1")

    out, _ = capsys.readouterr()
    assert "deleted" in out
    assert f"us-east1:{query_job.job_id}" in out
