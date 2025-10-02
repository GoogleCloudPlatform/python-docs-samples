# Copyright 2019 Google LLC
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

import pandas


def read_query_results() -> pandas.DataFrame:
    # [START bigquerystorage_pandas_tutorial_read_query_results]
    from google.cloud import bigquery

    bqclient = bigquery.Client()

    # Download query results.
    query_string = """
    SELECT
    CONCAT(
        'https://stackoverflow.com/questions/',
        CAST(id as STRING)) as url,
    view_count
    FROM `bigquery-public-data.stackoverflow.posts_questions`
    WHERE tags like '%google-bigquery%'
    ORDER BY view_count DESC
    """

    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_query_results]

    return dataframe
