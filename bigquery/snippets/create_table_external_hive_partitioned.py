# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def create_table_external_hive_partitioned(table_id: str) -> "bigquery.Table":
    original_table_id = table_id
    # [START bigquery_create_table_external_hivepartitioned]
    # Demonstrates creating an external table with hive partitioning.

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = "your-project.your_dataset.your_table_name"

    # TODO(developer): Set source uri.
    # Example file:
    # gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/dt=2020-11-15/file1.parquet
    uri = "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/*"

    # TODO(developer): Set source uri prefix.
    source_uri_prefix = (
        "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/"
    )

    # [END bigquery_create_table_external_hivepartitioned]
    table_id = original_table_id
    # [START bigquery_create_table_external_hivepartitioned]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Configure the external data source.
    external_config = bigquery.ExternalConfig("PARQUET")
    external_config.source_uris = [uri]
    external_config.autodetect = True

    # Configure partitioning options.
    hive_partitioning_opts = bigquery.HivePartitioningOptions()

    # The layout of the files in here is compatible with the layout requirements for hive partitioning,
    # so we can add an optional Hive partitioning configuration to leverage the object paths for deriving
    # partitioning column information.

    # For more information on how partitions are extracted, see:
    # https://cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs

    # We have a "/dt=YYYY-MM-DD/" path component in our example files as documented above.
    # Autolayout will expose this as a column named "dt" of type DATE.
    hive_partitioning_opts.mode = "AUTO"
    hive_partitioning_opts.require_partition_filter = True
    hive_partitioning_opts.source_uri_prefix = source_uri_prefix

    external_config.hive_partitioning = hive_partitioning_opts

    table = bigquery.Table(table_id)
    table.external_data_configuration = external_config

    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    # [END bigquery_create_table_external_hivepartitioned]
    return table
