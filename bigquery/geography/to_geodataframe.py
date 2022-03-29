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

from google.cloud import bigquery

if typing.TYPE_CHECKING:
    import pandas


client: bigquery.Client = bigquery.Client()


def get_austin_service_requests_as_geography() -> "pandas.DataFrame":
    # [START bigquery_query_results_geodataframe]

    sql = """
        SELECT created_date, complaint_description,
               ST_GEOGPOINT(longitude, latitude) as location
        FROM bigquery-public-data.austin_311.311_service_requests
        LIMIT 10
    """

    df = client.query(sql).to_geodataframe()
    # [END bigquery_query_results_geodataframe]
    return df
