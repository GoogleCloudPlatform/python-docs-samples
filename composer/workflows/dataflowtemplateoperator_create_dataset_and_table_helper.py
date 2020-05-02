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

# [START composer_dataflow_dataset_table_creation]

from google.cloud import bigquery

# [END composer_dataflow_dataset_table_creation]


def create_dataset(project, dataset_uuid):
    # [START composer_dataflow_dataset_table_creation]

    # Make sure to set your Google application credentials beforehand.
    # See instructions here: https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set project to your GCP Project ID.
    # project = "your-client-project"

    dataset_id = f"{project}.average_weather"

    # [END composer_dataflow_dataset_table_creation]

    # dataset_id is being reassigned here in order to test dataset creation
    # with a unique uuid in the _test.py file.
    dataset_id = f"{project}.{dataset_uuid}"

    # [START composer_dataflow_dataset_table_creation]

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    # TODO(developer): Fill out this location appropriately.
    # dataset.location = your-data-location

    # Send the dataset to the API for creation.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset)  # Make an API request.

    print(f"Created dataset {client.project}.{dataset.dataset_id}")
    # [END composer_dataflow_dataset_table_creation]

    return dataset


def create_table(project, dataset_id):

    client = bigquery.Client()
    # [START composer_dataflow_dataset_table_creation]

    # Create a table from this dataset.

    table_id = f"{client.project}.average_weather.average_weather"

    # [END composer_dataflow_dataset_table_creation]

    # table_id is being reassigned here in order to test table creation
    # with a unique uuid in the _test.py file.
    table_id = f"{client.project}.{dataset_id}.average_weather"

    # [START composer_dataflow_dataset_table_creation]
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
    return table
