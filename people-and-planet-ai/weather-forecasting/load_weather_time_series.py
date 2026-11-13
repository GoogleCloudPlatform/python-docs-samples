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

# [START dataflow_weather_load_time_series]
from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta, timezone
import math
import sys
from typing import Any

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from google.api_core import exceptions
from google.cloud import bigquery


def compute_melissa_hourly_rainfall(hour_offset: int) -> float:
    """Computes the Hurricane Melissa rainfall rate (mm/hr) at `hour_offset`.

    Models outer spiral rainbands, the Category 5 eyewall peak at hour `+35`
    (`2025-10-28 17:00 UTC`), and post-landfall orographic lift over Jamaica's
    Blue Mountains (`+36..+41`).

    Args:
        hour_offset: Integer hours elapsed since `2025-10-27 06:00 UTC`.

    Returns:
        Hourly precipitation rate in mm/hr rounded to 2 decimal places.
    """
    eyewall_pulse = 44.5 * math.exp(-(((hour_offset - 35.0) / 4.2) ** 2))
    outer_bands = 6.5 * math.exp(-(((hour_offset - 22.0) / 10.0) ** 2))
    orographic_tail = 14.0 * math.exp(-(((hour_offset - 39.0) / 6.5) ** 2))
    diurnal_ripple = 1.4 * math.sin(hour_offset * 0.65)
    return max(
        0.2,
        round(
            1.2 + outer_bands + eyewall_pulse + orographic_tail + diurnal_ripple,
            2,
        ),
    )


class _BuildHourlyObservationFn(beam.DoFn):
    """Transforms an hourly storm offset into a BigQuery observation record.

    Models outer rainbands, eyewall landfall peak at hour +35 (17:00 UTC Oct 28),
    and post-landfall orographic rainfall over Jamaica's Blue Mountains so
    each hourly window is computed in parallel across Apache Beam workers.
    """

    def process(self, hour_offset: int) -> Iterable[dict[str, Any]]:
        base_time = datetime(2025, 10, 27, 6, 0, 0, tzinfo=timezone.utc)
        obs_time = base_time + timedelta(hours=hour_offset)
        precip_mm_hr = compute_melissa_hourly_rainfall(hour_offset)
        cloud_moisture_index = round(min(1.0, 0.35 + 0.62 * (precip_mm_hr / 52.0)), 3)
        yield {
            "observation_time": obs_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "storm_name": "Hurricane Melissa",
            "location_name": "Jamaica (18.1N, 78.0W)",
            "latitude": 18.1,
            "longitude": -78.0,
            "precipitation_mm_hr": precip_mm_hr,
            "cloud_moisture_index": cloud_moisture_index,
            "elevation_m": 1120.0,
        }


def load_weather_time_series(
    project_id: str,
    dataset_id: str,
    table_id: str,
    beam_args: list[str] | None = None,
) -> None:
    """Loads hourly storm satellite observations into BigQuery with Apache Beam.

    Transforms a sequence of hourly storm observation windows into structured
    precipitation, cloud moisture, and terrain elevation records and writes
    them to a BigQuery table for downstream time-series forecasting.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        dataset_id: BigQuery dataset identifier (for example, 'example_dataset').
        table_id: BigQuery table identifier (for example, 'storm_observations').
        beam_args: Optional Apache Beam pipeline command-line arguments.
    """
    bq_client = bigquery.Client(project=project_id)
    dataset_ref = f"{project_id}.{dataset_id}"
    table_spec = f"{project_id}:{dataset_id}.{table_id}"
    hour_offsets = list(range(36))

    table_schema = (
        "observation_time:TIMESTAMP,storm_name:STRING,location_name:STRING,"
        "latitude:FLOAT64,longitude:FLOAT64,precipitation_mm_hr:FLOAT64,"
        "cloud_moisture_index:FLOAT64,elevation_m:FLOAT64"
    )
    pipeline_options = PipelineOptions(beam_args, save_main_session=True)

    try:
        bq_client.create_dataset(dataset_ref, exists_ok=True)
        print(f"Running Apache Beam pipeline to populate {table_id}...")
        with beam.Pipeline(options=pipeline_options) as pipeline:
            (
                pipeline
                | "SeedHourOffsets" >> beam.Create(hour_offsets)
                | "BuildHourlyRecords" >> beam.ParDo(_BuildHourlyObservationFn())
                | "WriteToBigQuery"
                >> beam.io.WriteToBigQuery(
                    table=table_spec,
                    schema=table_schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    method=beam.io.WriteToBigQuery.Method.FILE_LOADS,
                )
            )
    except (exceptions.GoogleAPICallError, RuntimeError) as err:
        print(
            f"error: failed to load weather time series into table "
            f"'{table_id}': {err}",
            file=sys.stderr,
        )
    else:
        print(f"Display Name: {table_id}")
        print(f"Dataset ID: {dataset_id}")
        print(f"Loaded Hours: {len(hour_offsets)}")
        print("Storm Name: Hurricane Melissa")


# [END dataflow_weather_load_time_series]


if __name__ == "__main__":
    import argparse
    import logging
    import os

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        description="Load hourly storm weather observations into BigQuery."
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID.",
    )
    parser.add_argument(
        "--dataset",
        default="weather_forecasting",
        help="BigQuery dataset ID.",
    )
    parser.add_argument(
        "--table",
        default="storm_hourly_observations",
        help="BigQuery table ID.",
    )
    known_args, pipeline_args = parser.parse_known_args()
    load_weather_time_series(
        project_id=known_args.project,
        dataset_id=known_args.dataset,
        table_id=known_args.table,
        beam_args=pipeline_args,
    )
