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


def client_list_jobs(client):

    # [START bigquery_list_jobs]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    import datetime

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # List the 10 most recent jobs in reverse chronological order.
    # Omit the max_results parameter to list jobs from the past 6 months.
    print("Last 10 jobs:")
    for job in client.list_jobs(max_results=10):  # API request(s)
        print("{}".format(job.job_id))

    # The following are examples of additional optional parameters:

    # Use min_creation_time and/or max_creation_time to specify a time window.
    print("Jobs from the last ten minutes:")
    ten_mins_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    for job in client.list_jobs(min_creation_time=ten_mins_ago):
        print("{}".format(job.job_id))

    # Use all_users to include jobs run by all users in the project.
    print("Last 10 jobs run by all users:")
    for job in client.list_jobs(max_results=10, all_users=True):
        print("{} run by user: {}".format(job.job_id, job.user_email))

    # Use state_filter to filter by job state.
    print("Last 10 jobs done:")
    for job in client.list_jobs(max_results=10, state_filter="DONE"):
        print("{}".format(job.job_id))
    # [END bigquery_list_jobs]
