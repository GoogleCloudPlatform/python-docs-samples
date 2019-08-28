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


def query_to_arrow(client):

    # [START bigquery_query_to_arrow]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    sql = """
    WITH races AS (
    SELECT "800M" AS race,
        [STRUCT("Rudisha" as name, [23.4, 26.3, 26.4, 26.1] as splits),
        STRUCT("Makhloufi" as name, [24.5, 25.4, 26.6, 26.1] as splits),
        STRUCT("Murphy" as name, [23.9, 26.0, 27.0, 26.0] as splits),
        STRUCT("Bosse" as name, [23.6, 26.2, 26.5, 27.1] as splits),
        STRUCT("Rotich" as name, [24.7, 25.6, 26.9, 26.4] as splits),
        STRUCT("Lewandowski" as name, [25.0, 25.7, 26.3, 27.2] as splits),
        STRUCT("Kipketer" as name, [23.2, 26.1, 27.3, 29.4] as splits),
        STRUCT("Berian" as name, [23.7, 26.1, 27.0, 29.3] as splits)]
        AS participants)
    SELECT
    race,
    participant
    FROM races r
    CROSS JOIN UNNEST(r.participants) as participant;
    """
    query_job = client.query(sql)
    arrow_table = query_job.to_arrow()

    print(
        "Downloaded {} rows, {} columns.".format(
            arrow_table.num_rows, arrow_table.num_columns
        )
    )
    print("\nSchema:\n{}".format(repr(arrow_table.schema)))
    # [END bigquery_query_to_arrow]
    return arrow_table
