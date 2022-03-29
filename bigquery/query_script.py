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


def query_script() -> None:
    # [START bigquery_query_script]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Run a SQL script.
    sql_script = """
    -- Declare a variable to hold names as an array.
    DECLARE top_names ARRAY<STRING>;

    -- Build an array of the top 100 names from the year 2017.
    SET top_names = (
    SELECT ARRAY_AGG(name ORDER BY number DESC LIMIT 100)
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE year = 2000
    );

    -- Which names appear as words in Shakespeare's plays?
    SELECT
    name AS shakespeare_name
    FROM UNNEST(top_names) AS name
    WHERE name IN (
    SELECT word
    FROM `bigquery-public-data.samples.shakespeare`
    );
    """
    parent_job = client.query(sql_script)

    # Wait for the whole script to finish.
    rows_iterable = parent_job.result()
    print("Script created {} child jobs.".format(parent_job.num_child_jobs))

    # Fetch result rows for the final sub-job in the script.
    rows = list(rows_iterable)
    print(
        "{} of the top 100 names from year 2000 also appear in Shakespeare's works.".format(
            len(rows)
        )
    )

    # Fetch jobs created by the SQL script.
    child_jobs_iterable = client.list_jobs(parent_job=parent_job)
    for child_job in child_jobs_iterable:
        child_rows = list(child_job.result())
        print(
            "Child job with ID {} produced {} row(s).".format(
                child_job.job_id, len(child_rows)
            )
        )

    # [END bigquery_query_script]
