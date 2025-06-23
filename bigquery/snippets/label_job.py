# Copyright 2025 Google LLC
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


def label_job() -> None:
    # [START bigquery_label_job]
    from google.cloud import bigquery

    client = bigquery.Client()

    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    labels = {"color": "green"}

    config = bigquery.QueryJobConfig()
    config.labels = labels
    location = "us"
    job = client.query(sql, location=location, job_config=config)
    job_id = job.job_id

    print(f"Added {job.labels} to {job_id}.")
    # [END bigquery_label_job]
