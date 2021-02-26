# Copyright 2021 Google LLC
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
import subprocess
import uuid

from google.cloud import bigquery
from google.cloud import storage
import pytest

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"wildlife-insights-test-{SUFFIX}"
BIGQUERY_DATASET = f"wildlife_insights_test_{SUFFIX}"
BIGQUERY_TABLE = "images_database"
REGION = "us-central1"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    yield BUCKET_NAME

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    bigquery_client = bigquery.Client()

    dataset_id = f"{PROJECT}.{BIGQUERY_DATASET}"
    bigquery_client.create_dataset(bigquery.Dataset(dataset_id))

    yield BIGQUERY_DATASET

    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def bigquery_table(bucket_name: str, bigquery_dataset: str) -> None:
    # Create the images database table.
    subprocess.run(
        [
            "python",
            "pipeline.py",
            "--create-images-database",
            f"--project={PROJECT}",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={BIGQUERY_TABLE}",
            "--runner=DataflowRunner",
            f"--region={REGION}",
            "--worker_machine_type=n1-standard-2",
        ],
        check=True,
    )

    # The table is deleted when we delete the dataset.
    yield BIGQUERY_TABLE


def test_end_to_end(
    bucket_name: str, bigquery_dataset: str, bigquery_table: str
) -> None:
    subprocess.run(
        [
            "python",
            "pipeline_test.py",
            f"--project={PROJECT}",
            f"--region={REGION}",
            f"--bucket={bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={bigquery_table}",
        ],
        check=True,
    )
