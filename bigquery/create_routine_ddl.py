# Copyright 2019 Google LLC
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


def create_routine_ddl(client, routine_id):

    # [START bigquery_create_routine_ddl]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Choose a fully-qualified ID for the routine.
    # routine_id = "my-project.my_dataset.my_routine"

    sql = """
    CREATE FUNCTION `{}`(
        arr ARRAY<STRUCT<name STRING, val INT64>>
    ) AS (
        (SELECT SUM(IF(elem.name = "foo",elem.val,null)) FROM UNNEST(arr) AS elem)
    )
    """.format(
        routine_id
    )

    # Initiate the query to create the routine.
    query_job = client.query(sql)

    # Wait for the query to complete.
    query_job.result()

    print("Created routine {}".format(query_job.ddl_target_routine))
    # [END bigquery_create_routine_ddl]
