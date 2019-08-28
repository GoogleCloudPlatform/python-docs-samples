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


def create_job(client):

    # [START bigquery_create_job]
    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    query_job = client.query(
        "SELECT country_name from `bigquery-public-data.utility_us.country_code_iso`",
        # Explicitly force job execution to be routed to a specific processing
        # location.
        location="US",
        # Specify a job configuration to set optional job resource properties.
        job_config=bigquery.QueryJobConfig(
            labels={"example-label": "example-value"}, maximum_bytes_billed=1000000
        ),
        # The client libraries automatically generate a job ID. Override the
        # generated ID with either the job_id_prefix or job_id parameters.
        job_id_prefix="code_sample_",
    )  # API request

    print("Started job: {}".format(query_job.job_id))
    # [END bigquery_create_job]
    return query_job
