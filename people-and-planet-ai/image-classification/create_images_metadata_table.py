#!/usr/bin/env python

# Copyright 2026 Google LLC
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

# [START dataflow_wildlife_ingest_metadata]
from __future__ import annotations

from collections.abc import Iterable
import io
import json
import os
import sys
import time
import zipfile

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.api_core import exceptions
import requests

METADATA_URL = (
    "https://storage.googleapis.com/public-datasets-lila/wcs/wcs_camera_traps.json.zip"
)

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


class _ExtractMetadataFn(beam.DoFn):
    """Downloads and parses camera trap image annotations from LILA Science."""

    def process(self, metadata_url: str) -> Iterable[dict[str, str]]:
        content = b""
        for attempt in range(3):
            try:
                content = requests.get(metadata_url, timeout=120).content
                break
            except requests.RequestException:
                if attempt == 2:
                    raise
                time.sleep(2**attempt)

        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            filename = os.path.splitext(os.path.basename(metadata_url))[0]
            with archive.open(filename) as metadata_file:
                metadata = json.load(metadata_file)

        categories = {
            category["id"]: category["name"]
            for category in metadata["categories"]
        }
        file_names = {
            image["id"]: image["file_name"] for image in metadata["images"]
        }

        for annotation in metadata["annotations"]:
            category_id = annotation["category_id"]
            image_id = annotation["image_id"]
            if category_id not in categories or image_id not in file_names:
                continue
            category_name = categories[category_id]
            if (
                category_name in INVALID_CATEGORIES
                or category_name.startswith("unknown ")
                or category_name.endswith(" desconocida")
                or category_name.endswith(" desconocido")
            ):
                continue
            yield {
                "category": category_name,
                "file_name": file_names[image_id],
            }


def create_images_metadata_table(
    project_id: str,
    bigquery_dataset: str,
    bigquery_table: str,
    pipeline_options: PipelineOptions | None = None,
) -> None:
    """Ingests LILA WCS camera trap image metadata into a BigQuery table.

    Reads the Wildlife Conservation Society (WCS) Camera Traps metadata archive
    from the public LILA Science Cloud Storage bucket, filters out unannotated
    or ambiguous records, and writes the species category and relative image
    path to BigQuery.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        bigquery_dataset: BigQuery dataset identifier where the table is stored.
        bigquery_table: BigQuery table identifier to create or overwrite.
        pipeline_options: Optional Apache Beam pipeline execution configuration.
    """
    table_spec = f"{project_id}:{bigquery_dataset}.{bigquery_table}"
    schema = "category:STRING,file_name:STRING"

    try:
        with beam.Pipeline(options=pipeline_options) as pipeline:
            (
                pipeline
                | "SeedMetadataUrl" >> beam.Create([METADATA_URL])
                | "ParseValidAnnotations" >> beam.ParDo(_ExtractMetadataFn())
                | "WriteMetadataToBigQuery"
                >> beam.io.WriteToBigQuery(
                    table=table_spec,
                    schema=schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                )
            )
    except (exceptions.GoogleAPICallError, RuntimeError) as err:
        print(
            f"error: failed to populate BigQuery table '{table_spec}' for "
            f"project '{project_id}': {err}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {table_spec}")
        print(f"BigQuery Dataset: {bigquery_dataset}")
        print(f"BigQuery Table: {bigquery_table}")
        print(f"Metadata Archive: {METADATA_URL}")
# [END dataflow_wildlife_ingest_metadata]


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID.",
    )
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

    options = PipelineOptions(
        pipeline_args, project=args.project, save_main_session=True
    )
    create_images_metadata_table(
        project_id=args.project,
        bigquery_dataset=args.bigquery_dataset,
        bigquery_table=args.bigquery_table,
        pipeline_options=options,
    )
