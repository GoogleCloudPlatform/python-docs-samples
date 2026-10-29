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

# [START dataflow_wildlife_run_inference]
from __future__ import annotations

from collections.abc import Iterable, Sequence
import sys
from typing import Any

import apache_beam as beam
from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import RunInference
from apache_beam.options.pipeline_options import PipelineOptions
from google import genai
from google.api_core import exceptions
from google.genai import errors
from google.genai import types
from pydantic import BaseModel

LILA_WCS_GCS_PREFIX = "gs://public-datasets-lila/wcs-unzipped"


class WildlifeObservation(BaseModel):
    species_scientific_name: str
    taxon_family: str
    common_name: str
    animal_count: int
    juvenile_present: bool
    is_empty_or_misfire: bool
    confidence: float


class GeminiWildlifeModelHandler(
    ModelHandler[dict[str, str], dict[str, Any], genai.Client]
):
    """Beam ModelHandler that classifies camera trap images with Gemini."""

    def __init__(self, project_id: str) -> None:
        self._project_id = project_id

    def load_model(self) -> genai.Client:
        return genai.Client(
            vertexai=True, project=self._project_id, location="global"
        )

    def run_inference(
        self,
        batch: Sequence[dict[str, str]],
        model: genai.Client,
        inference_args: dict[str, Any] | None = None,
    ) -> Iterable[dict[str, Any]]:
        prompt = (
            "Identify the wildlife species (scientific name, taxonomic family, "
            "and common name) in this camera trap photo, count the individuals, "
            "indicate whether juvenile offspring are present, and flag whether "
            "the frame is empty or a camera misfire."
        )
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=WildlifeObservation,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW,
            ),
        )
        for item in batch:
            image_gcs_uri = f"{LILA_WCS_GCS_PREFIX}/{item['file_name']}"
            image_part = types.Part.from_uri(
                file_uri=image_gcs_uri,
                mime_type="image/jpeg",
            )
            response = model.models.generate_content(
                model="gemini-3.8-flash",
                contents=[image_part, prompt],
                config=config,
            )
            obs = WildlifeObservation.model_validate_json(response.text)
            yield {
                "image_gcs_uri": image_gcs_uri,
                "ground_truth_category": item["category"],
                "species_scientific_name": obs.species_scientific_name,
                "taxon_family": obs.taxon_family,
                "common_name": obs.common_name,
                "animal_count": obs.animal_count,
                "juvenile_present": obs.juvenile_present,
                "is_empty_or_misfire": obs.is_empty_or_misfire,
                "confidence": obs.confidence,
            }


def run_wildlife_inference(
    project_id: str,
    bigquery_dataset: str,
    source_table: str,
    predictions_table: str,
    min_images_per_class: int = 1,
    max_images_per_class: int = 5,
    pipeline_options: PipelineOptions | None = None,
) -> None:
    """Runs class-balanced camera trap inference with Apache Beam RunInference.

    Samples a balanced set of camera trap records per species from BigQuery,
    classifies each image in-place from the public LILA Science Cloud Storage
    bucket using Gemini 3.8 Flash inside Apache Beam RunInference, and writes
    the structured ecological observations to BigQuery.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        bigquery_dataset: BigQuery dataset identifier containing the tables.
        source_table: Source BigQuery table containing 'category' and 'file_name'.
        predictions_table: Destination BigQuery table for structured predictions.
        min_images_per_class: Minimum images required to include a species class.
        max_images_per_class: Maximum images sampled per species class.
        pipeline_options: Optional Apache Beam pipeline execution configuration.
    """
    source_spec = f"{project_id}:{bigquery_dataset}.{source_table}"
    dest_spec = f"{project_id}:{bigquery_dataset}.{predictions_table}"
    output_schema = ",".join(
        [
            "image_gcs_uri:STRING",
            "ground_truth_category:STRING",
            "species_scientific_name:STRING",
            "taxon_family:STRING",
            "common_name:STRING",
            "animal_count:INTEGER",
            "juvenile_present:BOOLEAN",
            "is_empty_or_misfire:BOOLEAN",
            "confidence:FLOAT",
        ]
    )
    model_handler = GeminiWildlifeModelHandler(project_id=project_id)

    try:
        with beam.Pipeline(options=pipeline_options) as pipeline:
            (
                pipeline
                | "ReadMetadataFromBigQuery"
                >> beam.io.ReadFromBigQuery(table=source_spec)
                | "KeyBySpecies" >> beam.WithKeys(lambda row: row["category"])
                | "SamplePerSpecies"
                >> beam.combiners.Sample.FixedSizePerKey(max_images_per_class)
                | "DropKey" >> beam.Values()
                | "FilterMinImages"
                >> beam.Filter(
                    lambda sample: len(sample) >= min_images_per_class
                )
                | "FlattenSampledRows"
                >> beam.FlatMap(lambda sample: sample)
                | "RunGeminiInference" >> RunInference(model_handler)
                | "WritePredictionsToBigQuery"
                >> beam.io.WriteToBigQuery(
                    table=dest_spec,
                    schema=output_schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                )
            )
    except (exceptions.GoogleAPICallError, errors.APIError) as err:
        print(
            f"error: failed to run wildlife inference pipeline writing to "
            f"'{dest_spec}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {dest_spec}")
        print(f"Max Images Per Class: {max_images_per_class}")
        print(f"Min Images Per Class: {min_images_per_class}")
        print(f"Source Table: {source_spec}")
# [END dataflow_wildlife_run_inference]


if __name__ == "__main__":
    import argparse
    import logging
    import os

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
        help="BigQuery dataset ID.",
    )
    parser.add_argument(
        "--bigquery-table",
        default="wildlife_images_metadata",
        help="Source BigQuery metadata table ID.",
    )
    parser.add_argument(
        "--predictions-table",
        default="wildlife_predictions",
        help="Destination BigQuery table ID for structured Gemini predictions.",
    )
    parser.add_argument(
        "--min-images-per-class",
        type=int,
        default=1,
        help="Minimum number of images required per class.",
    )
    parser.add_argument(
        "--max-images-per-class",
        type=int,
        default=5,
        help="Maximum number of images sampled per class.",
    )
    args, pipeline_args = parser.parse_known_args()

    options = PipelineOptions(
        pipeline_args, project=args.project, save_main_session=True
    )
    run_wildlife_inference(
        project_id=args.project,
        bigquery_dataset=args.bigquery_dataset,
        source_table=args.bigquery_table,
        predictions_table=args.predictions_table,
        min_images_per_class=args.min_images_per_class,
        max_images_per_class=args.max_images_per_class,
        pipeline_options=options,
    )
