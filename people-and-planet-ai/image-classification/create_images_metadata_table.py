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

from __future__ import annotations

from collections.abc import Iterable
import io
import json
import logging
import os
import zipfile

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests

METADATA_URL = "https://lilablobssc.blob.core.windows.net/wcs/wcs_camera_traps.json.zip"

INVALID_CATEGORIES = {
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


def run(
    bigquery_dataset: str,
    bigquery_table: str,
    pipeline_options: PipelineOptions | None = None,
) -> None:
    """Creates the images metadata table in BigQuery.

    This is a one time only process. It reads the metadata file from the LILA
    science WCS database, gets rid of invalid rows and uploads all the
    `file_names` alongside their respective `category` into BigQuery.

    To learn more about the WCS Camera Traps dataset:
        http://lila.science/datasets/wcscameratraps

    Args:
        bigquery_dataset: Dataset ID for the images database, the dataset must exist.
        bigquery_table: Table ID for the images database, it is created if it doesn't exist.
        pipeline_options: PipelineOptions for Apache Beam.
    """
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
            | "Create None" >> beam.Create([METADATA_URL])
            | "Get images info" >> beam.FlatMap(get_images_metadata)
            | "Filter invalid rows"
            >> beam.Filter(
                lambda x: x"] not in INVALID_CATEGORIES
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


def get_images_metadata(metadata_url: str) -> Iterable[dict[str, str]]:
    """Returns an iterable of {'category', 'file_name'} dicts. """
    content = requests.get(metadata_url).content
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        filename = os.path.splitext(os.path.basename(metadata_url))[0]
        with zf.open(filename) as f:
            metadata = json.load(f)

    categories = {
        category["id"]: category"] for category in metadata["categories"]
    }
    file_names = {image["id"]: image"] for image in metadata["images"]}

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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bigquery-dataset",
        required=True,
        help="BigQuery dataset ID for the images metadata.",
    )
    parser.add_argument(
        "--bigquery-table",
        default="wildlife_images_metadata",
        help="BigQuery table ID for the images metadata.",
    )
    args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args, save_main_session=True)
    run(args.bigquery_dataset, args.bigquery_table, pipeline_options)
