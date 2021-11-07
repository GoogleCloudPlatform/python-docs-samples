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

import io
import os
import subprocess
import uuid

from google.cloud import aiplatform
from google.cloud import bigquery
from google.cloud import storage
import pytest

import deploy_model
import predict

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"wildlife-insights-{SUFFIX}"
BIGQUERY_DATASET = f"wildlife_insights_{SUFFIX}"
BIGQUERY_TABLE = "images_database"
MODEL_ENDPOINT = f"wildlife_insights_{SUFFIX}"
REGION = "us-central1"
MIN_IMAGES_PER_CLASS = 1
MAX_IMAGES_PER_CLASS = 1

# Use a pre-trained pre-existing model, training one takes too long.
MODEL_PATH = f"projects/{PROJECT}/locations/{REGION}/models/8785722428534816768"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    print(f"bucket_name: {repr(BUCKET_NAME)}")
    yield BUCKET_NAME

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    bigquery_client = bigquery.Client()

    dataset_id = f"{PROJECT}.{BIGQUERY_DATASET}"
    bigquery_client.create_dataset(bigquery.Dataset(dataset_id))

    print(f"bigquery_dataset: {repr(BIGQUERY_DATASET)}")
    yield BIGQUERY_DATASET

    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def bigquery_table(bigquery_dataset: str) -> str:
    # Create a small test table.
    table_id = f"{PROJECT}.{bigquery_dataset}.{BIGQUERY_TABLE}"
    schema = [
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("file_name", "STRING"),
    ]
    rows = [
        "alectoris rufa,animals/0059/1810.jpg",
        "equus quagga,animals/0378/0118.jpg",
        "fossa fossana,animals/0620/0242.jpg",
        "human,humans/0379/0877.jpg",
        "human,humans/0640/0467.jpg",
        "lophotibis cristataa,animals/0605/1478.jpg",
        "mazama temama,animals/0532/0525.jpg",
        "odontophorus balliviani,animals/0523/1368.jpg",
        "tayassu pecari,animals/0049/0849.jpg",
        "tayassu pecari,animals/0090/1218.jpg",
    ]

    bigquery_client = bigquery.Client()
    with io.StringIO("\n".join(rows)) as source_file:
        bigquery_client.load_table_from_file(
            source_file,
            table_id,
            job_config=bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                schema=schema,
            ),
        ).result()

    # The table is deleted when we delete the dataset.
    table = bigquery_client.get_table(table_id)
    print(f"bigquery_table: {repr(BIGQUERY_TABLE)}")
    print(f"    table_id: {repr(table_id)}")
    print(f"    num_rows: {repr(table.num_rows)}")
    print(f"    schema: {repr(table.schema)}")
    yield BIGQUERY_TABLE


@pytest.fixture(scope="session")
def model_endpoint_id() -> str:
    print(f"model_path: {repr(MODEL_PATH)}")
    endpoint_id = deploy_model.create_model_endpoint(PROJECT, REGION, MODEL_ENDPOINT)
    deployed_model_id = deploy_model.deploy_model(
        PROJECT, REGION, MODEL_PATH, MODEL_ENDPOINT, endpoint_id
    )

    print(f"model_endpoint_id: {repr(endpoint_id)}")
    yield endpoint_id

    client = aiplatform.gapic.EndpointServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    endpoint_path = client.endpoint_path(PROJECT, REGION, endpoint_id)
    client.undeploy_model(
        endpoint=endpoint_path, deployed_model_id=deployed_model_id
    ).result()
    client.delete_endpoint(name=endpoint_path).result()


def test_create_images_database_table(bucket_name: str, bigquery_dataset: str) -> None:
    # The table is deleted when we delete the dataset.
    subprocess.run(
        [
            "python",
            "create_images_metadata_table.py",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={BIGQUERY_TABLE}_test",
            "--runner=DataflowRunner",
            f"--job_name=wildlife-images-database-{SUFFIX}",
            f"--project={PROJECT}",
            f"--temp_location=gs://{bucket_name}/temp",
            f"--region={REGION}",
            "--worker_machine_type=n1-standard-2",
        ],
        check=True,
    )


def test_train_model(
    bucket_name: str, bigquery_dataset: str, bigquery_table: str
) -> None:
    subprocess.run(
        [
            "python",
            "train_model.py",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={bigquery_table}",
            "--ai-platform-name-prefix=",  # empty skips the AI Platform operations.
            f"--min-images-per-class={MIN_IMAGES_PER_CLASS}",
            f"--max-images-per-class={MAX_IMAGES_PER_CLASS}",
            "--runner=DataflowRunner",
            f"--job_name=wildlife-train-{SUFFIX}",
            f"--project={PROJECT}",
            f"--temp_location=gs://{bucket_name}/temp",
            "--requirements_file=requirements.txt",
            f"--region={REGION}",
        ],
        check=True,
    )


def test_predict(model_endpoint_id: str) -> None:
    predictions = predict.run(
        project=PROJECT,
        region=REGION,
        model_endpoint_id=model_endpoint_id,
        image_file="animals/0036/0072.jpg",  # tapirus indicus
    )
    assert len(predictions) > 0, f"predictions: {repr(predictions)}"
