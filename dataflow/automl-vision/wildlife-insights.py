#!/usr/bin/env python

# Copyright 2020 Google LLC
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

import argparse
import io
import json
import logging
import os
import random
import requests
import time
import zipfile
from PIL import Image, ImageFile

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import trainingjob


def init(bigquery_dataset, bigquery_table, pipeline_options=None):
    invalid_categories = {
        "empty",
        "#ref!",
        "unidentifiable",
        "start",
        "end",
        "unidentified",
        "unknown",
    }

    # https://cloud.google.com/bigquery/docs/schemas
    schema = ",".join(
        [
            "category:STRING",
            "file_name:STRING",
        ]
    )

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "Create single element" >> beam.Create([None])
            | "Get images info" >> beam.FlatMap(get_images_info)
            | "Filter invalid categories"
            >> beam.Filter(lambda x: x["category"] not in invalid_categories)
            | "Write images info"
            >> beam.io.WriteToBigQuery(
                dataset=bigquery_dataset,
                table=bigquery_table,
                schema=schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


def get_images_info(_):
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


def train_model(
    project,
    region,
    cloud_storage_path,
    bigquery_dataset,
    bigquery_table,
    automl_model_name,
    min_images_per_class,
    max_images_per_class,
    automl_budget_milli_node_hours,
    pipeline_options=None,
):
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
                automl_model_name=automl_model_name,
            )
            | "Import images" >> beam.MapTuple(import_images_to_automl_dataset)
            | "Train AutoML model"
            >> beam.Map(
                train_automl_model,
                project=project,
                region=region,
                automl_model_name=automl_model_name,
                automl_budget_milli_node_hours=automl_budget_milli_node_hours,
            )
        )


def get_image(image_info, cloud_storage_path):
    base_url = "https://lilablobssc.blob.core.windows.net/wcs-unzipped"
    category = image_info["category"]
    file_name = image_info["file_name"]

    # If the image file does not exist, try downloading it.
    image_path = f"{cloud_storage_path}/{file_name}"
    if not beam.io.gcp.gcsio.GcsIO().exists(image_path):
        image_url = f"{base_url}/{file_name}"
        logging.info(f"image not found, downloading: {image_path} [{image_url}]")
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            image = Image.open(io.BytesIO(url_get(image_url)))
            with beam.io.gcp.gcsio.GcsIO().open(image_path, "w") as f:
                image.save(f, format="JPEG")
        except Exception as e:
            logging.warning(f"Failed to load image [{image_url}]: {e}")
            return

    yield category, image_path


def write_dataset_csv_file(dataset_csv_filename, images):
    # https://cloud.google.com/ai-platform-unified/docs/datasets/prepare-image#csv
    logging.info(f"Writing AutoML dataset CSV file: {dataset_csv_filename}")
    with beam.io.gcp.gcsio.GcsIO().open(dataset_csv_filename, "w") as f:
        for category, image_gcs_path in images:
            f.write(f"{image_gcs_path},{category}\n".encode("utf-8"))
    return dataset_csv_filename


def create_automl_dataset(dataset_csv_filename, project, region, automl_model_name):
    # https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#create-dataset
    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    # Return the dataset if it exists.
    datasets = client.list_datasets(
        parent=f"projects/{project}/locations/{region}",
    )
    for dataset in datasets:
        if dataset.display_name == automl_model_name:
            logging.info(f"AutoML dataset found: {dataset.name}\n{dataset}")
            return dataset.name, dataset_csv_filename

    # If no dataset was returned, then create it.
    logging.warning(f"AutoML dataset not found: {automl_model_name}")
    response = client.create_dataset(
        parent=f"projects/{project}/locations/{region}",
        dataset={
            "display_name": automl_model_name,
            "metadata_schema_uri": "gs://google-cloud-aiplatform/schema/dataset/metadata/image_1.0.0.yaml",
        },
    )
    logging.info(f"Creating AutoML dataset, operation: {response.operation.name}")
    dataset = response.result()  # wait until the operation finishes
    logging.info(f"AutoML dataset created: {dataset.name}\n{dataset}")
    return dataset.name, dataset_csv_filename


def import_images_to_automl_dataset(dataset_path, dataset_csv_filename):
    # https://cloud.google.com/ai-platform-unified/docs/datasets/create-dataset-api#import-data
    client = aiplatform.gapic.DatasetServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.import_data(
        name=dataset_path,
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
    logging.info(f"AutoML data imported: {dataset_path}")
    return dataset_path


def train_automl_model(
    dataset_path, project, region, automl_model_name, automl_budget_milli_node_hours
):
    # https://cloud.google.com/ai-platform-unified/docs/training/automl-api#training_an_automl_model_using_the_api
    client = aiplatform.gapic.PipelineServiceClient(
        client_options={
            "api_endpoint": "us-central1-aiplatform.googleapis.com",
        }
    )

    response = client.create_training_pipeline(
        parent=f"projects/{project}/locations/{region}",
        training_pipeline={
            "display_name": automl_model_name,
            "training_task_definition": "gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_image_classification_1.0.0.yaml",
            "training_task_inputs": trainingjob.definition.AutoMlImageClassificationInputs(
                model_type="CLOUD",
                budget_milli_node_hours=automl_budget_milli_node_hours,
            ).to_value(),
            "input_data_config": {"dataset_id": dataset_path.split("/")[-1]},
            "model_to_upload": {"display_name": automl_model_name},
        },
    )
    logging.info(f"Training AutoML model, training pipeline: {response.name}")
    logging.info(f"{response}")
    return response.name


def url_get(url):
    logging.info(f"url_get: {url}")
    return with_retries(lambda: requests.get(url).content)


def with_retries(f, max_attempts=3):
    # https://developers.google.com/drive/api/v3/handle-errors?hl=pt-pt#exponential-backoff
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init",
        action="store_true",
        help="Creates a BigQuery table and initializes it with the WCS metadata file entries",
    )
    parser.add_argument("--cloud-storage-bucket", required=True)
    parser.add_argument("--bigquery-dataset", required=True)
    parser.add_argument("--bigquery-table", default="wildlife_insights")
    parser.add_argument("--automl-model-name", default="wildlife_insights")
    parser.add_argument("--min-images-per-class", type=int, default=50)
    parser.add_argument("--max-images-per-class", type=int, default=80)
    parser.add_argument("--automl-budget-milli-node-hours", type=int, default=8000)
    args, pipeline_args = parser.parse_known_args()

    cloud_storage_path = f"gs://{args.cloud_storage_bucket}/samples/wildlife-insights"
    pipeline_options = PipelineOptions(
        pipeline_args,
        temp_location=f"{cloud_storage_path}/temp",
        save_main_session=True,
    )
    project = pipeline_options.get_all_options().get("project")
    if not project:
        parser.error("please provide a Google Cloud project ID: --project")
    region = pipeline_options.get_all_options().get("region")
    if not region:
        parser.error("please provide a Google Cloud compute region: --region")

    if args.init:
        init(
            bigquery_dataset=args.bigquery_dataset,
            bigquery_table=args.bigquery_table,
            pipeline_options=pipeline_options,
        )

    else:
        train_model(
            project=project,
            region=region,
            cloud_storage_path=args.cloud_storage_path,
            bigquery_dataset=args.bigquery_dataset,
            bigquery_table=args.bigquery_table,
            automl_model_name=args.automl_model_name,
            min_images_per_class=args.min_images_per_class,
            max_images_per_class=args.max_images_per_class,
            automl_budget_milli_node_hours=args.automl_budget_milli_node_hours,
            pipeline_options=pipeline_options,
        )
