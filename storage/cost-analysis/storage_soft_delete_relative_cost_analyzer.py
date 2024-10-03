#!/usr/bin/env python

# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Identifies buckets with relative increase in cost on enabling the soft-delete.

The relative increase in cost of using soft delete is calculated by combining
the storage/v2/deleted_bytes metric with the existing
storage/v2/total_byte_seconds
metric.

Relative cost of each bucket = deleted_bytes / total_byte_seconds
                                 x Soft delete retention duration-seconds
                                 x Relative Storage Cost
                                 x Storage Class Ratio
"""
# [START storage_soft_delete_relative_cost]
from __future__ import annotations

import argparse
import json
import google.cloud.monitoring_v3 as monitoring_client


def get_relative_cost(storage_class: str) -> float:
    """Retrieves the relative cost for a given storage class and location.

    Args:
        storage_class: The storage class (e.g., 'standard', 'nearline').

    Returns:
        The price per GB from the https://cloud.google.com/storage/pricing,
        divided by the standard storage class.
    """
    relative_cost = {
        "STANDARD": 0.023 / 0.023,
        "NEARLINE": 0.013 / 0.023,
        "COLDLINE": 0.007 / 0.023,
        "ARCHIVE": 0.0025 / 0.023,
    }

    return relative_cost.get(storage_class, 1.0)


def get_soft_delete_cost(
    project_name: str,
    soft_delete_window: float,
    agg_days: int,
    lookback_days: int,
) -> dict[str, list[dict[str, float]]]:
    """Calculates soft delete costs for buckets in a Google Cloud project.

    Args:
        project_name: The name of the Google Cloud project.
        soft_delete_window: The time window in seconds for considering
          soft-deleted objects (default is 7 days).
        agg_days: Aggregate results over a time period, defaults to 30-day period
        lookback_days: Look back up to upto days, defaults to 360 days

    Returns:
        A dictionary with bucket names as keys and cost data for each bucket,
        broken down by storage class.
    """

    query_client = monitoring_client.QueryServiceClient()

    # Step 1: Get storage class ratios for each bucket.
    storage_ratios_by_bucket = get_storage_class_ratio(
        project_name, query_client, agg_days, lookback_days
    )

    # Step 2: Fetch soft-deleted bytes and calculate costs using Monitoring API.
    soft_deleted_costs = calculate_soft_delete_costs(
        project_name,
        query_client,
        soft_delete_window,
        storage_ratios_by_bucket,
        agg_days,
        lookback_days,
    )

    return soft_deleted_costs


def calculate_soft_delete_costs(
    project_name: str,
    query_client: monitoring_client.QueryServiceClient,
    soft_delete_window: float,
    storage_ratios_by_bucket: dict[str, float],
    agg_days: int,
    lookback_days: int,
) -> dict[str, list[dict[str, float]]]:
    """Calculates the relative cost of enabling soft delete for each bucket in a
       project for certain time frame in secs.

    Args:
        project_name: The name of the Google Cloud project.
        query_client: A Monitoring API query client.
        soft_delete_window: The time window in seconds for considering
          soft-deleted objects (default is 7 days).
        storage_ratios_by_bucket: A dictionary of storage class ratios per bucket.
        agg_days: Aggregate results over a time period, defaults to 30-day period
        lookback_days: Look back up to upto days, defaults to 360 days

    Returns:
        A dictionary with bucket names as keys and a list of cost data
        dictionaries
        for each bucket, broken down by storage class.
    """
    soft_deleted_bytes_time = query_client.query_time_series(
        monitoring_client.QueryTimeSeriesRequest(
            name=f"projects/{project_name}",
            query=f"""
                    {{  # Fetch 1: Soft-deleted (bytes seconds)
                        fetch gcs_bucket :: storage.googleapis.com/storage/v2/deleted_bytes
                        | value val(0) * {soft_delete_window}\'s\'  # Multiply by soft delete window
                        | group_by [resource.bucket_name, metric.storage_class], window(), .sum;

                        # Fetch 2: Total byte-seconds (active objects)
                        fetch gcs_bucket :: storage.googleapis.com/storage/v2/total_byte_seconds
                        | filter metric.type != 'soft-deleted-object'
                        | group_by [resource.bucket_name, metric.storage_class], window(1d), .mean  # Daily average
                        | group_by [resource.bucket_name, metric.storage_class], window(), .sum  # Total over window

                    }}  # End query definition
                    | every {agg_days}d  # Aggregate over larger time intervals
                    | within {lookback_days}d  # Limit data range for analysis
                    | ratio  # Calculate ratio (soft-deleted (bytes seconds)/ total (bytes seconds))
                    """,
        )
    )

    buckets: dict[str, list[dict[str, float]]] = {}
    missing_distribution_storage_class = []
    for data_point in soft_deleted_bytes_time.time_series_data:
        bucket_name = data_point.label_values[0].string_value
        storage_class = data_point.label_values[1].string_value
        # To include location-based cost analysis:
        # 1. Uncomment the line below:
        # location = data_point.label_values[2].string_value
        # 2. Update how you calculate 'relative_storage_class_cost' to factor in location
        soft_delete_ratio = data_point.point_data[0].values[0].double_value
        distribution_storage_class = bucket_name + " - " + storage_class
        storage_class_ratio = storage_ratios_by_bucket.get(
            distribution_storage_class
        )
        if storage_class_ratio is None:
            missing_distribution_storage_class.append(
                distribution_storage_class)
        buckets.setdefault(bucket_name, []).append({
            # Include storage class and location data for additional plotting dimensions.
            # "storage_class": storage_class,
            # 'location': location,
            "soft_delete_ratio": soft_delete_ratio,
            "storage_class_ratio": storage_class_ratio,
            "relative_storage_class_cost": get_relative_cost(storage_class),
        })

    if missing_distribution_storage_class:
        print(
            "Missing storage class for following buckets:",
            missing_distribution_storage_class,
        )
        raise ValueError("Cannot proceed with missing storage class ratios.")

    return buckets


def get_storage_class_ratio(
    project_name: str,
    query_client: monitoring_client.QueryServiceClient,
    agg_days: int,
    lookback_days: int,
) -> dict[str, float]:
    """Calculates storage class ratios for each bucket in a project.

    This information helps determine the relative cost contribution of each
    storage class to the overall soft-delete cost.

    Args:
        project_name: The Google Cloud project name.
        query_client: Google Cloud's Monitoring Client's QueryServiceClient.
        agg_days: Aggregate results over a time period, defaults to 30-day period
        lookback_days: Look back up to upto days, defaults to 360 days

    Returns:
        Ratio of Storage classes within a bucket.
    """
    request = monitoring_client.QueryTimeSeriesRequest(
        name=f"projects/{project_name}",
        query=f"""
            {{
            # Fetch total byte-seconds for each bucket and storage class
            fetch gcs_bucket :: storage.googleapis.com/storage/v2/total_byte_seconds
            | group_by [resource.bucket_name, metric.storage_class], window(), .sum;
            # Fetch total byte-seconds for each bucket (regardless of class)
            fetch gcs_bucket :: storage.googleapis.com/storage/v2/total_byte_seconds
            | group_by [resource.bucket_name], window(), .sum
            }}
            | ratio  # Calculate ratios of storage class size to total size
            | every {agg_days}d
            | within {lookback_days}d
            """,
    )

    storage_class_ratio = query_client.query_time_series(request)

    storage_ratios_by_bucket = {}
    for time_series in storage_class_ratio.time_series_data:
        bucket_name = time_series.label_values[0].string_value
        storage_class = time_series.label_values[1].string_value
        ratio = time_series.point_data[0].values[0].double_value

        # Create a descriptive key for the dictionary
        key = f"{bucket_name} - {storage_class}"
        storage_ratios_by_bucket[key] = ratio

    return storage_ratios_by_bucket


def soft_delete_relative_cost_analyzer(
    project_name: str,
    cost_threshold: float = 0.0,
    soft_delete_window: float = 604800,
    agg_days: int = 30,
    lookback_days: int = 360,
    list_buckets: bool = False,
    ) -> str | dict[str, float]: # Note potential string output
    """Identifies buckets exceeding the relative cost threshold for enabling soft delete.

    Args:
        project_name: The Google Cloud project name.
        cost_threshold: Threshold above which to consider removing soft delete.
        soft_delete_window: Time window for calculating soft-delete costs (in
          seconds).
        agg_days: Aggregate results over this time period (in days).
        lookback_days: Look back up to this many days.
        list_buckets: Return a list of bucket names (True) or JSON (False,
          default).

    Returns:
        JSON formatted results of buckets exceeding the threshold and costs
        *or* a space-separated string of bucket names.
    """

    buckets: dict[str, float] = {}
    for bucket_name, storage_sources in get_soft_delete_cost(
        project_name, soft_delete_window, agg_days, lookback_days
    ).items():
        bucket_cost = 0.0
        for storage_source in storage_sources:
            bucket_cost += (
                storage_source["soft_delete_ratio"]
                * storage_source["storage_class_ratio"]
                * storage_source["relative_storage_class_cost"]
            )
        if bucket_cost > cost_threshold:
            buckets[bucket_name] = round(bucket_cost, 4)

    if list_buckets:
        return " ".join(buckets.keys())  # Space-separated bucket names
    else:
        return json.dumps(buckets, indent=2)  # JSON output


def soft_delete_relative_cost_analyzer_main() -> None:
    # Sample run: python storage_soft_delete_relative_cost_analyzer.py <Project Name>
    parser = argparse.ArgumentParser(
        description="Analyze and manage Google Cloud Storage soft-delete costs."
    )
    parser.add_argument(
        "project_name", help="The name of the Google Cloud project to analyze."
    )
    parser.add_argument(
        "--cost_threshold",
        type=float,
        default=0.0,
        help="Relative Cost threshold.",
    )
    parser.add_argument(
        "--soft_delete_window",
        type=float,
        default=604800.0,
        help="Time window (in seconds) for considering soft-deleted objects.",
    )
    parser.add_argument(
        "--agg_days",
        type=int,
        default=30,
        help=(
            "Time window (in days) for aggregating results over a time period,"
            " defaults to 30-day period"
        ),
    )
    parser.add_argument(
        "--lookback_days",
        type=int,
        default=360,
        help=(
            "Time window (in days) for considering the how old the bucket to be."
        ),
    )
    parser.add_argument(
        "--list",
        type=bool,
        default=False,
        help="Return the list of bucketnames seperated by space.",
    )

    args = parser.parse_args()

    response = soft_delete_relative_cost_analyzer(
        args.project_name,
        args.cost_threshold,
        args.soft_delete_window,
        args.agg_days,
        args.lookback_days,
        args.list,
    )
    if not args.list:
        print(
            "To remove soft-delete policy from the listed buckets run:\n"
            # Capture output
            "python storage_soft_delete_relative_cost_analyzer.py"
            " [your-project-name] --[OTHER_OPTIONS] --list > list_of_buckets.txt \n"
            "cat list_of_buckets.txt | gcloud storage buckets update -I "
            "--clear-soft-delete",
            response,
        )
        return
    print(response)


if __name__ == "__main__":
    soft_delete_relative_cost_analyzer_main()
# [END storage_soft_delete_relative_cost]
