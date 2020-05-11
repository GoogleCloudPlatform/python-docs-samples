# Copyright 2020 Google LLC
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

# This script is a helper function to the Dataflow Template Operator Tutorial.
# It helps the user set up a BigQuery dataset and table that is needed
# for the tutorial.

import argparse

# [START composer_dataflow_dataset_table_creation]

# Make sure to follow the quickstart setup instructions beforehand.
# See instructions here:
# https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries

# Before running the sample, be sure to install the bigquery library
# in your local environment by running pip install google.cloud.bigquery

# If you choose to download the library, you can also run the sample with the
#  following command:
#    python dataflowtemplateoperator_create_dataset_and_table_helper.py \
#    PROJECT_ID \
#    LOCATION
#   where `PROJECT_ID` is your Google Cloud Project ID and `LOCATION` is where you
#   want the location of your BigQuery dataset.

from google.cloud import bigquery


def create_dataset_and_table(project, location, dataset_name):
    # Construct a BigQuery client object.
    client = bigquery.Client(project)

    dataset_id = f"{project}.{dataset_name}"

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    # Set the location to your desired location for the dataset. 
    # For more information, see this link:
    # https://cloud.google.com/bigquery/docs/locations
    dataset.location = location

    # Send the dataset to the API for creation.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset)  # Make an API request.

    print(f"Created dataset {client.project}.{dataset.dataset_id}")

    # Create a table from this dataset.

    table_id = f"{client.project}.{dataset_name}.average_weather"

    schema = [
        bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
        bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
        bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE"),
    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    # [END composer_dataflow_dataset_table_creation]
    return dataset, table


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create BQ dataset and table")
    parser.add_argument("project", metavar="P", type=str, help="your GCP project ID")
    parser.add_argument(
        "location",
        metavar="L",
        type=str,
        help='where your dataset should reside (i.e., "U.S."',
    )
    args = parser.parse_args()
    create_dataset_and_table(args.project, args.location, "average_weather")
