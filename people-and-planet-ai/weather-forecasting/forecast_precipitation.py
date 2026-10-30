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

# [START bigquery_weather_forecast_precipitation]
import os
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def forecast_precipitation(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Forecasts hourly precipitation using BigQuery ML AI.FORECAST with TimesFM.

    Executes zero-shot time-series forecasting directly in BigQuery using the
    TimesFM 2.5 foundation model to predict upcoming hourly rainfall rates and
    90% prediction intervals without training a custom model.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        dataset_id: BigQuery dataset identifier (for example, 'example_dataset').
        table_id: BigQuery source table ID (for example, 'storm_hourly_observations').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    forecast_horizon = 6
    confidence_level = 0.90

    query = f"""
        SELECT
          forecast_timestamp,
          forecast_value AS forecasted_precipitation_mm_hr,
          prediction_interval_lower_bound AS lower_bound_mm_hr,
          prediction_interval_upper_bound AS upper_bound_mm_hr
        FROM
          AI.FORECAST(
            TABLE `{table_ref}`,
            data_col => 'precipitation_mm_hr',
            timestamp_col => 'observation_time',
            model => 'TimesFM 2.5',
            id_cols => ['storm_name'],
            horizon => {forecast_horizon},
            confidence_level => {confidence_level}
          )
        ORDER BY
          forecast_timestamp ASC
    """

    try:
        query_job = client.query(query)
        print(
            f"Waiting for BigQuery AI.FORECAST job {query_job.job_id} to complete..."
        )
        forecast_rows = list(query_job.result())
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to run AI.FORECAST on table '{table_ref}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        peak_forecast = max(
            (float(row.forecasted_precipitation_mm_hr) for row in forecast_rows),
            default=0.0,
        )
        print(f"Resource ID: {table_ref}")
        print(f"Display Name: {table_id}")
        print(f"Confidence Level: {confidence_level:.2f}")
        print(f"Forecast Horizon Hours: {len(forecast_rows)}")
        print(f"Peak Forecasted Precipitation (mm/hr): {peak_forecast:.2f}")
        for row in forecast_rows:
            ts_str = row.forecast_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            val = float(row.forecasted_precipitation_mm_hr)
            low = max(0.0, float(row.lower_bound_mm_hr))
            high = float(row.upper_bound_mm_hr)
            print(
                f"  {ts_str}: {val:.2f} mm/hr "
                f"(90% CI: [{low:.2f}, {high:.2f}] mm/hr)"
            )


# [END bigquery_weather_forecast_precipitation]


project_id_arg = os.environ.get("GOOGLE_CLOUD_PROJECT") or (
    sys.argv[1] if len(sys.argv) > 1 else None
)
if not project_id_arg:
    project_id_arg = "example-project-id"

dataset_id_arg = os.environ.get("BIGQUERY_DATASET") or (
    sys.argv[2] if len(sys.argv) > 2 else None
)
if not dataset_id_arg:
    dataset_id_arg = "weather_forecasting"

table_id_arg = os.environ.get("BIGQUERY_TABLE") or (
    sys.argv[3] if len(sys.argv) > 3 else None
)
if not table_id_arg:
    table_id_arg = "storm_hourly_observations"

if __name__ == "__main__":
    forecast_precipitation(project_id_arg, dataset_id_arg, table_id_arg)
