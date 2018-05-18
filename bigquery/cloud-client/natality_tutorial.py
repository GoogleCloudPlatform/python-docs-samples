#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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


def run_natality_tutorial():
    # [START bigquery_query_natality_tutorial]
    """Create a Google BigQuery linear regression input table.

    In the code below, the following actions are taken:
    * A new dataset is created "natality_regression."
    * A new table "regression_input" is created to hold the inputs for our
        linear regression.
    * A query is run against the public dataset,
        bigquery-public-data.samples.natality, selecting only the data of
        interest to the regression, the output of which is stored in the
        "regression_input" table.
    * The output table is moved over the wire to the user's default project via
        the built-in BigQuery Connector for Spark that bridges BigQuery and
        Cloud Dataproc.
    """

    from google.cloud import bigquery

    # Create a new Google BigQuery client using Google Cloud Platform project
    # defaults.
    client = bigquery.Client()

    # The name for the new dataset.
    dataset_id = 'natality_regression'

    # Prepare a reference to the new dataset.
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)

    # Create the new BigQuery dataset.
    dataset = client.create_dataset(dataset)

    # In the new BigQuery dataset, create a new table.
    table_ref = dataset.table('regression_input')
    # The table needs a schema before it can be created and accept data.
    # Create an ordered list of the columns using SchemaField objects.
    schema = [
        bigquery.SchemaField('weight_pounds', 'float'),
        bigquery.SchemaField('mother_age', 'integer'),
        bigquery.SchemaField('father_age', 'integer'),
        bigquery.SchemaField('gestation_weeks', 'integer'),
        bigquery.SchemaField('weight_gain_pounds', 'integer'),
        bigquery.SchemaField('apgar_5min', 'integer'),
    ]

    # Assign the schema to the table and create the table in BigQuery.
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)

    # Set up a query in Standard SQL, which is the default for the BigQuery
    # Python client library.
    # The query selects the fields of interest.
    query = """
        SELECT weight_pounds, mother_age, father_age, gestation_weeks,
        weight_gain_pounds, apgar_5min
        FROM `bigquery-public-data.samples.natality`
        WHERE weight_pounds is not null
        and mother_age is not null and father_age is not null
        and gestation_weeks is not null
        and weight_gain_pounds is not null
        and apgar_5min is not null
    """
    # Configure the query job.
    job_config = bigquery.QueryJobConfig()
    # Set the output table to the table created above.
    dest_dataset_ref = client.dataset('natality_regression')
    dest_table_ref = dest_dataset_ref.table('regression_input')
    job_config.destination = dest_table_ref

    # Run the query.
    query_job = client.query(query, job_config=job_config)
    query_job.result()  # Waits for the query to finish
    # [END bigquery_query_natality_tutorial]


if __name__ == '__main__':
    run_natality_tutorial()
