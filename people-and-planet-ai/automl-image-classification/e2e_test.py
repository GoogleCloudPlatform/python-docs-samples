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

from dataclasses import dataclass
import os
import subprocess
from typing import Any
import uuid

from google.cloud import bigquery
from google.cloud import storage
import pytest

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
BUCKET_NAME = f"wildlife-insights-test-{SUFFIX}"
BIGQUERY_DATASET = f"wildlife_insights_test_{SUFFIX}"
BIGQUERY_TABLE = "images_database"
AUTOML_DATASET = "wildlife_insights_test"
AUTOML_MODEL = "wildlife_insights_test"
MIN_IMAGES_PER_CLASS = 0
MAX_IMAGES_PER_CLASS = 0


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

    py_code = f"""
from apache_beam.options.pipeline_options import PipelineOptions
import mock
import pipeline

@dataclass
class MockOperation:
    name: str = "operation_path"

@dataclass
class MockResponse:
    name: str

@dataclass
class MockRequest:
    def __init__(self: Any, name: str) -> None:
        self.name = "{{name}}_request"
        self._response_name = "{{name}}_response"
        self.operation = MockOperation()

    def result(self: Any) -> MockResponse:
        return MockResponse(self._response_name)

@mock.patch(
    "google.cloud.aiplatform_v1.services.dataset_service.DatasetServiceClient.create_dataset",
    lambda *args, **kwargs: MockRequest("create_dataset"),
)
@mock.patch(
    "google.cloud.aiplatform_v1.services.dataset_service.DatasetServiceClient.import_data",
    lambda *args, **kwargs: MockRequest("import_data"),
)
@mock.patch(
    "google.cloud.aiplatform_v1.services.pipeline_service.PipelineServiceClient.create_training_pipeline",
    lambda *args, **kwargs: MockRequest("create_training_pipeline"),
)
def run_mock_pipeline():
    pipeline_args = [
        "--project={PROJECT}",
        "--runner=DataflowRunner",
        "--requirements_file=requirements.txt",
        "--region={REGION}",
    ]
    pipeline_options = PipelineOptions(
        pipeline_args,
        temp_location="gs://{bucket_name}/temp",
        save_main_session=True,
    )

    pipeline.run(
        project=PROJECT,
        region=REGION,
        cloud_storage_path="gs://{bucket_name}",
        bigquery_dataset=bigquery_dataset,
        bigquery_table=bigquery_table,
        automl_dataset=AUTOML_DATASET,
        automl_model=AUTOML_MODEL,
        min_images_per_class=MIN_IMAGES_PER_CLASS,
        max_images_per_class=MAX_IMAGES_PER_CLASS,
        automl_budget_milli_node_hours=8000,
        pipeline_options=pipeline_options,
    )
run_mock_pipeline()"""

    subprocess.run(
        ["python", "-c", py_code],
        check=True,
    )