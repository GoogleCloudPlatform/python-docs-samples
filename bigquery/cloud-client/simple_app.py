#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Simple application that performs a query with BigQuery."""

# [START bigquery_simple_app_all]
import argparse

# [START bigquery_simple_app_deps]
import google_auth_oauthlib
from google.cloud import bigquery
# [END bigquery_simple_app_deps]


def authenticate(client_id, client_secret):
    # [START bigquery_simple_app_authenticate]
    # TODO(developer): Set the client ID and client secret to the values
    #                  identifying your application.
    # client_id = "YOUR-CLIENT-ID.apps.googleusercontent.com"
    # client_secret = "abc_ThIsIsAsEcReT"

    # This function opens a browser window to authenticate to your Google Cloud
    # Platform account. See the Google Cloud Platform Auth Guide for how to
    # authenticate your application in non-interactive contexts:
    # https://cloud.google.com/docs/authentication/
    credentials = google_auth_oauthlib.get_user_credentials(
        ["https://www.googleapis.com/auth/cloud-platform"],
        client_id,
        client_secret,
    )
    # [END bigquery_simple_app_authenticate]
    return credentials


def query_stackoverflow(credentials, project_id):
    # [START bigquery_simple_app_client]
    # TODO(developer): Set the project ID to the project used for billing.
    # project_id = "my-billing-project-id"

    client = bigquery.Client(credentials=credentials, project=project_id)
    # [END bigquery_simple_app_client]
    # [START bigquery_simple_app_query]
    query_job = client.query("""
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    # [END bigquery_simple_app_query]

    # [START bigquery_simple_app_print]
    # Download the full query results as a pandas DataFrame.
    df = results.to_dataframe()
    print(df)
    # [END bigquery_simple_app_print]


def main(project_id, client_id, client_secret):
    credentials = authenticate(client_id, client_secret)
    query_stackoverflow(credentials, project_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Sample BigQuery Application")
    parser.add_argument("project_id")
    parser.add_argument("client_id")
    parser.add_argument("client_secret")
    args = parser.parse_args()
    main(args.project_id, args.client_id, args.client_secret)
# [END bigquery_simple_app_all]
