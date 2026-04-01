# Copyright 2026 Google LLC
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
from typing import Generator

from google.cloud import bigquery
import pytest
import test_utils.prefixer

import read_gbq_function

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
prefixer = test_utils.prefixer.Prefixer("python-docs-samples", "bigquery/dataframes")


@pytest.fixture(scope="module")
def bq_client() -> bigquery.Client:
    return bigquery.Client(project=PROJECT_ID)


@pytest.fixture(scope="module")
def dataset_id(bq_client: bigquery.Client) -> Generator[str, None, None]:
    dataset_name = prefixer.create_prefix().replace("-", "_")
    dataset_id = f"{PROJECT_ID}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    bq_client.create_dataset(dataset)
    yield dataset_id
    bq_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="module")
def udf_id(bq_client: bigquery.Client, dataset_id: str) -> str:
    function_id = f"{dataset_id}.extract_title"
    query = f"""
    CREATE OR REPLACE FUNCTION `{function_id}`(xml STRING) RETURNS STRING AS (
      SAFE.REGEXP_EXTRACT(xml, r'<title>(.*?)</title>')
    );
    """
    bq_client.query(query).result()
    return function_id


def test_use_read_gbq_function(
    capsys: pytest.CaptureFixture[str], udf_id: str
) -> None:
    read_gbq_function.use_read_gbq_function(PROJECT_ID, udf_id)
    out, _ = capsys.readouterr()

    assert "The Great Gatsby" in out
    assert "1984" in out
    assert "Brave New World" in out
