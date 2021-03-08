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
REGION = "us-central1"
MIN_IMAGES_PER_CLASS = 1
MAX_IMAGES_PER_CLASS = 1
AUTOML_MODEL_PATH = ""


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    yield BUCKET_NAME

    # This test creates 1 image file per class, creating around 650 files.
    # `bucket.delete(force=True)` does not work if the bucket has >256 files.
    # Sequentially deleting many files with the client libraries can take
    # several minutes, so we're using `gsutil -m` instead.
    # subprocess.call(["gsutil", "-m", "rm", "-rf", f"gs://{BUCKET_NAME}/*"])
    bucket.delete(force=True)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    bigquery_client = bigquery.Client()

    dataset_id = f"{PROJECT}.{BIGQUERY_DATASET}"
    bigquery_client.create_dataset(bigquery.Dataset(dataset_id))

    yield BIGQUERY_DATASET

    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def bigquery_table(bigquery_dataset: str) -> str:
    # Create a small test table.
    data = """category,file_name
alectoris rufa,animals/0059/1810.jpg
equus quagga,animals/0378/0118.jpg
fossa fossana,animals/0620/0242.jpg
human,humans/0379/0877.jpg
human,humans/0640/0467.jpg
lophotibis cristataa,animals/0605/1478.jpg
mazama temama,animals/0532/0525.jpg
odontophorus balliviani,animals/0523/1368.jpg
tayassu pecari,animals/0049/0849.jpg
tayassu pecari,animals/0090/1218.jpg"""

    bigquery_client = bigquery.Client()
    with io.StringIO(data) as source_file:
        job = bigquery_client.load_table_from_file(
            source_file,
            f"{PROJECT}.{bigquery_dataset}.{BIGQUERY_TABLE}",
            job_config=bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=True,
            ),
        )
        job.result()  # Waits for the job to complete.

    # The table is deleted when we delete the dataset.
    yield BIGQUERY_TABLE


@pytest.fixture(scope="session")
def model_endpoint_id() -> str:
    yield deploy_model.run(
        project=PROJECT,
        region=REGION,
        model_path=AUTOML_MODEL_PATH,
        model_endpoint_name="wildlife_insights",
    )


def test_create_images_database(bucket_name: str, bigquery_dataset: str) -> None:
    subprocess.run(
        [
            "python",
            "pipeline.py",
            "--create-images-database",
            f"--project={PROJECT}",
            f"--job_name=wildlife-images-database-{SUFFIX}",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={BIGQUERY_TABLE}",
            "--runner=DataflowRunner",
            f"--region={REGION}",
            "--worker_machine_type=n1-standard-2",
        ],
        check=True,
    )


def test_preprocess_data(
    bucket_name: str, bigquery_dataset: str, bigquery_table: str
) -> None:
    subprocess.run(
        [
            "python",
            "pipeline.py",
            f"--project={PROJECT}",
            f"--job_name=wildlife-train-{SUFFIX}",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={bigquery_table}",
            "--automl-name-prefix=",  # empty skips the AutoML operations.
            f"--min-images-per-class={MIN_IMAGES_PER_CLASS}",
            f"--max-images-per-class={MAX_IMAGES_PER_CLASS}",
            "--runner=DataflowRunner",
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
    assert len(predictions) > 0
