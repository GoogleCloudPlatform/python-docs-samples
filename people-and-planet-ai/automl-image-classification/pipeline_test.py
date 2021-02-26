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

# ---------------------------------------------------------------------------- #
# NOTE: This NOT a pytest file, it's used by e2e_test.py as a standalone script.
#
# AutoML operations take too long to finish, so we mock them to no-op functions.
# To run in Dataflow, it must be in a subprocess since pytest is unpicklable.
# ---------------------------------------------------------------------------- #

from typing import Any

from apache_beam.options.pipeline_options import PipelineOptions
import mock

import pipeline

AUTOML_DATASET = "wildlife_insights_test"
AUTOML_MODEL = "wildlife_insights_test"
MIN_IMAGES_PER_CLASS = 1
MAX_IMAGES_PER_CLASS = 1


class MockOperation:
    name: str = "operation_path"


class MockResponse:
    def __init__(self: Any, name: str) -> None:
        self.name = name


class MockRequest:
    def __init__(self: Any, name: str) -> None:
        self.name = f"{name}_request"
        self._response_name = f"{name}_response"
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
def run_mock_pipeline(
    project: str, region: str, bucket: str, bigquery_dataset: str, bigquery_table: str
) -> None:
    """Run the pipeline with mocked AutoML functions as no-op."""
    pipeline_args = [
        f"--project={project}",
        "--runner=DataflowRunner",
        "--requirements_file=requirements.txt",
        f"--region={region}",
    ]
    pipeline_options = PipelineOptions(
        pipeline_args,
        temp_location=f"gs://{bucket}/temp",
        save_main_session=True,
    )

    pipeline.run(
        project={project},
        cloud_storage_path=f"gs://{bucket}",
        bigquery_dataset=bigquery_dataset,
        bigquery_table=bigquery_table,
        automl_dataset=AUTOML_DATASET,
        automl_model=AUTOML_MODEL,
        min_images_per_class=MIN_IMAGES_PER_CLASS,
        max_images_per_class=MAX_IMAGES_PER_CLASS,
        automl_budget_milli_node_hours=8000,
        pipeline_options=pipeline_options,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--bigquery-dataset", required=True)
    parser.add_argument("--bigquery-table", required=True)
    args, pipeline_args = parser.parse_known_args()

    run_mock_pipeline(
        project=args.project,
        region=args.region,
        bucket=args.bucket,
        bigquery_dataset=args.bigquery_dataset,
        bigquery_table=args.bigquery_dataset,
    )
