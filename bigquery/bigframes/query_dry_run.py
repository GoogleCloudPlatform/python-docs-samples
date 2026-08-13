# Copyright 2026 Google LLC
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

# [START bigquery_bigframes_query_dry_run]
import bigframes.pandas as bpd

from google.cloud import bigquery


def query_dry_run() -> int:
    sql = """
    SELECT name, COUNT(*) as name_count
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'WA'
    GROUP BY name
    """

    session = bpd.get_global_session()
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Perform a dry run query using the session BigQuery client.
    query_job = session.bqclient.query(sql, job_config=job_config)

    # A dry run query completes immediately and returns query metadata.
    print(f"This query will process {query_job.total_bytes_processed} bytes.")
    return query_job.total_bytes_processed
# [END bigquery_bigframes_query_dry_run]


if __name__ == "__main__":
    query_dry_run()
