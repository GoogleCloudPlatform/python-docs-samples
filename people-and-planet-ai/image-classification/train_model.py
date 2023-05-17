#!/usr/bin/env python

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

from datetime import datetime
import io
import logging
import random
import time
from typing import Callable, Dict, Iterable, Optional, Tuple, TypeVar

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import trainingjob
from PIL import Image, ImageFile
import requests

a = TypeVar("a")


def run(
    project: str,
    region: str,
    cloud_storage_path: str,
    bigquery_dataset: str,
    bigquery_table: str,
    ai_platform_name_prefix: str,
    min_images_per_class: int,
    max_images_per_class: int,
    budget_milli_node_hours: int,
    pipeline_options: Optional[PipelineOptions] = None,
) -> None:
    """Creates a balanced dataset and signals AI Platform to train a model.

    Args:
        project: Google Cloud Project ID.
        region: Location for AI Platform resources.
        bigquery_dataset: Dataset ID for the images database, the dataset must exist.
        bigquery_table: Table ID for the images database, the table must exist.
        ai_platform_name_prefix: Name prefix for AI Platform resources.
        min_images_per_class: Minimum number of images required per class for training.
        max_images_per_class: Maximum number of images allowed per class for training.
        budget_milli_node_hours: Training budget.
        pipeline_options: PipelineOptions for Apache Beam.

    """
    with beam.Pipeline(options=pipeline_options) as pipeline:
        images = (
            pipeline
            | "Read images info"
            >> beam.io.ReadFromBigQuery(dataset=bigquery_dataset, table=bigquery_table)
            | "Key by category" >> beam.WithKeys(lambda x: x["category"])
            | "Random samples"
            >> beam.combiners.Sample.FixedSizePerKey(max_images_per_class)
            | "Remove key" >> beam.Values()
            | "Discard small samples"
            >> beam.Filter(lambda sample: len(sample) >= min_images_per_class)
            | "Flatten elements" >> beam.FlatMap(lambda sample: sample)
            | "Get image" >> beam.FlatMap(get_image, cloud_storage_path)
        )

        dataset_csv_filename = f"{cloud_storage_path}/dataset.csv"
        dataset_csv_file = (
            pipeline
            | "Dataset filename" >> beam.Create([dataset_csv_filename])
            | "Write dataset file"
            >> beam.Map(write_dataset_csv_file, images=beam.pvalue.AsIter(images))
        )

        if ai_platform_name_prefix:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            (
                dataset_csv_file
                | "Create dataset"
                >> beam.Map(
                    create_dataset,
                    project=project,
                    region=region,
                    dataset_name=f"{ai_platform_name_prefix}_{timestamp}",
                )
                | "Import images" >> beam.MapTuple(import_images_to_dataset)
                | "Train model"
                >> beam.Map(
                    train_model,
                    project=project,
                    region=region,
                    model_name=f"{ai_platform_name_prefix}_{timestamp}",
                    budget_milli_node_hours=budget_milli_node_hours,
                )
            )


def get_image(
    image_info: Dict[str, str], cloud_storage_path: str
) -> Iterable[Tuple[str, str]]:
    """Makes sure an image exists in Cloud Storage.

    Checks if the image file_name exists in Cloud Storage.
    If it doesn't exist, it downloads it from the LILA WCS dataset.
    If the image can't be downloaded, it is skipped.

    Args:
        image_info: Dict of {'category', 'file_name'}.
        cloud_storage_path: Cloud Storage path to look for and download images.

    Returns:
        A (category, image_gcs_path) tuple.
    """
    import apache_beam as beam

    base_url = "https://lilablobssc.blob.core.windows.net/wcs-unzipped"
    category = image_info["category"]
    file_name = image_info["file_name"]

    # If the image file does not exist, try downloading it.
    image_gcs_path = f"{cloud_storage_path}/{file_name}"
    logging.info(f"loading image: {image_gcs_path}")
    if not beam.io.gcp.gcsio.GcsIO().exists(image_gcs_path):
        image_url = f"{base_url}/{file_name}"
        logging.info(f"image not found, downloading: {image_gcs_path} [{image_url}]")
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            image = Image.open(io.BytesIO(url_get(image_url)))
            with beam.io.gcp.gcsio.GcsIO().open(image_gcs_path, "w") as f:
                image.save(f, format="JPEG")
        except Exception as e:
            logging.warning(f"Failed to load image [{image_url}]: {e}")
            return

    yield category, image_gcs_path


def write_dataset_csv_file(
    dataset_csv_filename: str, images: Iterable[Tuple[str, str]]
) -> str:
    """Writes the dataset image file names and categories in a CSV file.

    Each line in the output dataset CSV file is in the format:
        image_gcs_path,category

    For more information on the CSV format AI Platform expects:
        https://cloud.google.com/ai-platform-unified/docs/datasets/prepare-image#csv

    Args:
        dataset_csv_filename: Cloud Storage path for the output dataset CSV file.
        images: List of (category, image_gcs_path) tuples.

    Returns:
        The unchanged dataset_csv_filename.
    """
    import apache_beam as beam

    logging.info(f"Writing dataset CSV file: {dataset_csv_filename}")
    with beam.io.gcp.gcsio.GcsIO().open(dataset_csv_filename, "w") as f:
        for category, image_gcs_path in images:
            f.write(f"{image_gcs_path},{category}\n".encode())
    return dataset_csv_filename


def create_dataset(
    dataset_csv_filename: str, project: str, region: str, dataset_name: str
) -> Tuple[str, str]:
    """Creates an dataset for AI Platform.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#create-dataset

    Args:
        dataset_csv_filename: Cloud Storage path for the dataset CSV file.
        project: Google Cloud Project ID.
        region: Location for AI Platform resources.
        dataset_name: Dataset name.

    Returns:
        A (dataset_full_path, dataset_csv_filename) tuple.
    """
    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.create_dataset(
        parent=f"projects/{project}/locations/{region}",
        dataset={
            "display_name": dataset_name,
            "metadata_schema_uri": "gs://google-cloud-aiplatform/schema/dataset/metadata/image_1.0.0.yaml",
        },
    )
    logging.info(f"Creating dataset, operation: {response.operation.name}")
    dataset = response.result()  # wait until the operation finishes
    logging.info(f"Dataset created:\n{dataset}")
    return dataset.name, dataset_csv_filename


def import_images_to_dataset(dataset_full_path: str, dataset_csv_filename: str) -> str:
    """Imports the images from the dataset CSV file into the AI Platform dataset.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#import-data

    Args:
        dataset_full_path: The AI Platform dataset full path.
        dataset_csv_filename: Cloud Storage path for the dataset CSV file.

    Returns:
        The dataset_full_path.
    """
    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.import_data(
        name=dataset_full_path,
        import_configs=[
            {
                "gcs_source": {"uris": [dataset_csv_filename]},
                "import_schema_uri": "gs://google-cloud-aiplatform/schema/dataset/ioformat/image_classification_single_label_io_format_1.0.0.yaml",
            }
        ],
    )
    logging.info(f"Importing data into dataset, operation: {response.operation.name}")
    _ = response.result()  # wait until the operation finishes
    logging.info(f"Data imported: {dataset_full_path}")
    return dataset_full_path


def train_model(
    dataset_full_path: str,
    project: str,
    region: str,
    model_name: str,
    budget_milli_node_hours: int,
) -> str:
    """Starts a model training job.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/training/automl-api#training_an_automl_model_using_the_api

    Args:
        dataset_full_path: The AI Platform dataset full path.
        project: Google Cloud Project ID.
        region: Location for AI Platform resources.
        model_name: Model name.
        budget_milli_node_hours: Training budget.

    Returns:
        The training pipeline full path.
    """
    client = aiplatform.gapic.PipelineServiceClient(
        client_options={
            "api_endpoint": "us-central1-aiplatform.googleapis.com",
        }
    )

    training_pipeline = client.create_training_pipeline(
        parent=f"projects/{project}/locations/{region}",
        training_pipeline={
            "display_name": model_name,
            "input_data_config": {"dataset_id": dataset_full_path.split("/")[-1]},
            "model_to_upload": {"display_name": model_name},
            "training_task_definition": "gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_image_classification_1.0.0.yaml",
            "training_task_inputs": trainingjob.definition.AutoMlImageClassificationInputs(
                model_type="CLOUD",
                budget_milli_node_hours=budget_milli_node_hours,
            ).to_value(),
        },
    )
    logging.info(f"Training model, training pipeline:\n{training_pipeline}")
    return training_pipeline.name


def url_get(url: str) -> bytes:
    """Sends an HTTP GET request with retries.

    Args:
        url: URL for the request.

    Returns:
        The response content bytes.
    """
    logging.info(f"url_get: {url}")
    return with_retries(lambda: requests.get(url).content)


def with_retries(f: Callable[[], a], max_attempts: int = 3) -> a:
    """Runs a function with retries, using exponential backoff.

    For more information:
        https://developers.google.com/drive/api/v3/handle-errors?hl=pt-pt#exponential-backoff

    Args:
        f: A function that doesn't receive any input.
        max_attempts: The maximum number of attempts to run the function.

    Returns:
        The return value of `f`, or an Exception if max_attempts was reached.
    """
    for n in range(max_attempts + 1):
        try:
            return f()
        except Exception as e:
            if n < max_attempts:
                logging.warning(f"Got an error, {n+1} of {max_attempts} attempts: {e}")
                time.sleep(2**n + random.random())  # 2^n seconds + random jitter
            else:
                raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cloud-storage-path",
        required=True,
        help="Cloud Storage path to store the AI Platform dataset files.",
    )
    parser.add_argument(
        "--bigquery-dataset",
        required=True,
        help="BigQuery dataset ID for the images database.",
    )
    parser.add_argument(
        "--bigquery-table",
        default="wildlife_images_metadata",
        help="BigQuery table ID for the images database.",
    )
    parser.add_argument(
        "--ai-platform-name-prefix",
        default="wildlife_classifier",
        help="Name prefix for AI Platform resources.",
    )
    parser.add_argument(
        "--min-images-per-class",
        type=int,
        default=50,
        help="Minimum number of images required per class for training.",
    )
    parser.add_argument(
        "--max-images-per-class",
        type=int,
        default=80,
        help="Maximum number of images allowed per class for training.",
    )
    parser.add_argument(
        "--budget-milli-node-hours",
        type=int,
        default=8000,
        help="Training budget, see: https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#imageclassificationmodelmetadata",
    )
    args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args, save_main_session=True)
    project = pipeline_options.get_all_options().get("project")
    if not project:
        parser.error("please provide a Google Cloud project ID with --project")
    region = pipeline_options.get_all_options().get("region")
    if not region:
        parser.error("please provide a Google Cloud compute region with --region")

    run(
        project=project,
        region=region,
        cloud_storage_path=args.cloud_storage_path,
        bigquery_dataset=args.bigquery_dataset,
        bigquery_table=args.bigquery_table,
        ai_platform_name_prefix=args.ai_platform_name_prefix,
        min_images_per_class=args.min_images_per_class,
        max_images_per_class=args.max_images_per_class,
        budget_milli_node_hours=args.budget_milli_node_hours,
        pipeline_options=pipeline_options,
    )
