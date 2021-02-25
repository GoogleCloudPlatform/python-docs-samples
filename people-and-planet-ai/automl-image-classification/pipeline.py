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

import io
import json
import logging
import os
import random
import time
from typing import Any, Callable, Dict, Iterable, Optional, Tuple
import zipfile

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from PIL import Image, ImageFile
import requests


def create_images_database(
    bigquery_dataset: str,
    bigquery_table: str,
    pipeline_options: Optional[PipelineOptions] = None,
) -> None:
    """Creates the images database in BigQuery.

    This is a one time only process. It reads the metadata file from the LILA
    science WCS database, gets rid of invalid rows and uploads all the
    `file_names` alongside their respective `category` into BigQuery.

    Args:
        bigquery_dataset: Dataset ID for the images database, the dataset must exist.
        bigquery_table: Table ID for the images database, it is created if it doesn't exist.
        pipeline_options: PipelineOptions for Apache Beam.
    """
    invalid_categories = {
        "#ref!",
        "empty",
        "end",
        "misfire",
        "small mammal",
        "start",
        "unidentifiable",
        "unidentified",
        "unknown",
    }

    # We create a simple schema for the BigQuery table.
    # For more information on BigQuery schemas, see:
    #   https://cloud.google.com/bigquery/docs/schemas
    schema = ",".join(
        [
            "category:STRING",
            "file_name:STRING",
        ]
    )

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "Create None" >> beam.Create([None])
            | "Get images info" >> beam.FlatMap(get_images_info)
            | "Filter invalid rows"
            >> beam.Filter(
                lambda x: x["category"] not in invalid_categories
                or x["category"].startswith("unknown ")
                or x["category"].endswith(" desconocida")
                or x["category"].endswith(" desconocido")
            )
            | "Write images database"
            >> beam.io.WriteToBigQuery(
                dataset=bigquery_dataset,
                table=bigquery_table,
                schema=schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


def get_images_info(unused: Any) -> Iterable[Dict[str, str]]:
    """Returns an iterable of {'category', 'file_name'} dicts. """
    metadata_url = (
        "https://lilablobssc.blob.core.windows.net/wcs/wcs_camera_traps.json.zip"
    )

    content = url_get(metadata_url)
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        filename = os.path.splitext(os.path.basename(metadata_url))[0]
        with zf.open(filename) as f:
            metadata = json.load(f)

    categories = {
        category["id"]: category["name"] for category in metadata["categories"]
    }
    file_names = {image["id"]: image["file_name"] for image in metadata["images"]}

    for annotation in metadata["annotations"]:
        category_id = annotation["category_id"]
        image_id = annotation["image_id"]
        if category_id not in categories:
            logging.error(f"invalid category ID {category_id}, skipping")
        elif image_id not in file_names:
            logging.error(f"invalid image ID {image_id}, skipping")
        else:
            yield {
                "category": categories[category_id],
                "file_name": file_names[image_id],
            }


def run(
    project: str,
    region: str,
    cloud_storage_path: str,
    bigquery_dataset: str,
    bigquery_table: str,
    automl_dataset: str,
    automl_model: str,
    min_images_per_class: int,
    max_images_per_class: int,
    automl_budget_milli_node_hours: int,
    pipeline_options: Optional[PipelineOptions] = None,
) -> None:
    """Creates a balanced dataset and signals AutoML to train a model.

    Args:
        project: Google Cloud Project ID.
        region: Location for AutoML resources.
        bigquery_dataset: Dataset ID for the images database, the dataset must exist.
        bigquery_table: Table ID for the images database, the table must exist.
        automl_dataset: AutoML dataset name.
        automl_model: AutoML model name.
        min_images_per_class: Minimum number of images required per class for training.
        max_images_per_class: Maximum number of images allowed per class for training.
        automl_budget_milli_node_hours: Training budget.
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

        dataset_csv_filename = f"{cloud_storage_path}/automl-dataset.csv"
        (
            pipeline
            | "Dataset filename" >> beam.Create([dataset_csv_filename])
            | "Write dataset file"
            >> beam.Map(write_dataset_csv_file, images=beam.pvalue.AsIter(images))
            | "Create AutoML dataset"
            >> beam.Map(
                create_automl_dataset,
                project=project,
                region=region,
                automl_dataset=automl_dataset,
            )
            | "Import images" >> beam.MapTuple(import_images_to_automl_dataset)
            | "Train AutoML model"
            >> beam.Map(
                train_automl_model,
                project=project,
                region=region,
                automl_model=automl_model,
                automl_budget_milli_node_hours=automl_budget_milli_node_hours,
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

    For more information on the CSV format AutoML expects:
        https://cloud.google.com/ai-platform-unified/docs/datasets/prepare-image#csv

    Args:
        dataset_csv_filename: Cloud Storage path for the output dataset CSV file.
        images: List of (category, image_gcs_path) tuples.

    Returns:
        The unchanged dataset_csv_filename.
    """
    logging.info(f"Writing AutoML dataset CSV file: {dataset_csv_filename}")
    with beam.io.gcp.gcsio.GcsIO().open(dataset_csv_filename, "w") as f:
        for category, image_gcs_path in images:
            f.write(f"{image_gcs_path},{category}\n".encode("utf-8"))
    return dataset_csv_filename


def create_automl_dataset(
    dataset_csv_filename: str, project: str, region: str, automl_dataset: str
) -> Tuple[str, str]:
    """Creates an AutoML dataset.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#create-dataset

    Args:
        dataset_csv_filename: Cloud Storage path for the dataset CSV file.
        project: Google Cloud Project ID.
        region: Location for AutoML resources.
        automl_dataset: AutoML dataset name.

    Returns:
        A (automl_dataset_full_path, dataset_csv_filename) tuple.
    """
    from google.cloud import aiplatform

    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.create_dataset(
        parent=f"projects/{project}/locations/{region}",
        dataset={
            "display_name": automl_dataset,
            "metadata_schema_uri": "gs://google-cloud-aiplatform/schema/dataset/metadata/image_1.0.0.yaml",
        },
    )
    logging.info(f"Creating AutoML dataset, operation: {response.operation.name}")
    dataset = response.result()  # wait until the operation finishes
    logging.info(f"AutoML dataset created:\n{dataset}")
    return dataset.name, dataset_csv_filename


def import_images_to_automl_dataset(
    automl_dataset_full_path: str, dataset_csv_filename: str
) -> str:
    """Imports the images from the dataset CSV file into the AutoML dataset.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#import-data

    Args:
        automl_dataset_full_path: The AutoML dataset full path.
        dataset_csv_filename: Cloud Storage path for the dataset CSV file.

    Returns:
        The automl_dataset_full_path.
    """
    from google.cloud import aiplatform

    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.import_data(
        name=automl_dataset_full_path,
        import_configs=[
            {
                "gcs_source": {"uris": [dataset_csv_filename]},
                "import_schema_uri": "gs://google-cloud-aiplatform/schema/dataset/ioformat/image_classification_single_label_io_format_1.0.0.yaml",
            }
        ],
    )
    logging.info(
        f"Importing data into AutoML dataset, operation: {response.operation.name}"
    )
    _ = response.result()  # wait until the operation finishes
    logging.info(f"AutoML data imported: {automl_dataset_full_path}")
    return automl_dataset_full_path


def train_automl_model(
    automl_dataset_full_path: str,
    project: str,
    region: str,
    automl_model: str,
    automl_budget_milli_node_hours: int,
) -> str:
    """Starts an AutoML model training job.

    For more information:
        https://cloud.google.com/ai-platform-unified/docs/training/automl-api#training_an_automl_model_using_the_api

    Args:
        automl_dataset_full_path: The AutoML dataset full path.
        project: Google Cloud Project ID.
        region: Location for AutoML resources.
        automl_model: AutoML model name.
        automl_budget_milli_node_hours: Training budget.

    Returns:
        The AutoML training pipeline full path.
    """
    from google.cloud import aiplatform
    from google.cloud.aiplatform.gapic.schema import trainingjob

    client = aiplatform.gapic.PipelineServiceClient(
        client_options={
            "api_endpoint": "us-central1-aiplatform.googleapis.com",
        }
    )

    training_pipeline = client.create_training_pipeline(
        parent=f"projects/{project}/locations/{region}",
        training_pipeline={
            "display_name": automl_model,
            "input_data_config": {
                "dataset_id": automl_dataset_full_path.split("/")[-1]
            },
            "model_to_upload": {"display_name": automl_model},
            "training_task_definition": "gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_image_classification_1.0.0.yaml",
            "training_task_inputs": trainingjob.definition.AutoMlImageClassificationInputs(
                model_type="CLOUD",
                budget_milli_node_hours=automl_budget_milli_node_hours,
            ).to_value(),
        },
    )
    logging.info(f"Training AutoML model, training pipeline:\n{training_pipeline}")
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


def with_retries(f: Callable[[], Any], max_attempts: int = 3) -> Any:
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
                time.sleep(2 ** n + random.random())  # 2^n seconds + random jitter
            else:
                raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create-images-database",
        action="store_true",
        help="Creates a BigQuery table and initializes it with the WCS metadata file entries.",
    )
    parser.add_argument(
        "--cloud-storage-path",
        required=True,
        help="Cloud Storage path to store the AutoML dataset files.",
    )
    parser.add_argument(
        "--bigquery-dataset",
        required=True,
        help="BigQuery dataset ID for the images database.",
    )
    parser.add_argument(
        "--bigquery-table",
        default="wildlife_insights",
        help="BigQuery table ID for the images database.",
    )
    parser.add_argument(
        "--automl-dataset", default="wildlife_insights", help="AutoML dataset name."
    )
    parser.add_argument(
        "--automl-model", default="wildlife_insights", help="AutoML model name."
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
        "--automl-budget-milli-node-hours",
        type=int,
        default=8000,
        help="Training budget, see: https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#imageclassificationmodelmetadata",
    )
    args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(
        pipeline_args,
        temp_location=f"{args.cloud_storage_path}/temp",
        save_main_session=True,
    )
    project = pipeline_options.get_all_options().get("project")
    if not project:
        parser.error("please provide a Google Cloud project ID with --project")
    region = pipeline_options.get_all_options().get("region")
    if not region:
        parser.error("please provide a Google Cloud compute region with --region")

    if args.create_images_database:
        create_images_database(
            bigquery_dataset=args.bigquery_dataset,
            bigquery_table=args.bigquery_table,
            pipeline_options=pipeline_options,
        )

    else:
        run(
            project=project,
            region=region,
            cloud_storage_path=args.cloud_storage_path,
            bigquery_dataset=args.bigquery_dataset,
            bigquery_table=args.bigquery_table,
            automl_dataset=args.automl_dataset,
            automl_model=args.automl_model,
            min_images_per_class=args.min_images_per_class,
            max_images_per_class=args.max_images_per_class,
            automl_budget_milli_node_hours=args.automl_budget_milli_node_hours,
            pipeline_options=pipeline_options,
        )
