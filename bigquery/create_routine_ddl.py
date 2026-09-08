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


def create_routine_ddl(routine_id: str) -> None:
    # [START bigquery_create_routine_ddl]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

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
    query_job = client.query(sql)  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    print("Created routine {}".format(query_job.ddl_target_routine))
    # [END bigquery_create_routine_ddl]
