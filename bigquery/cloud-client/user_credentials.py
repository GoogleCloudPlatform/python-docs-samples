#!/usr/bin/env python

# Copyright 2017 Google Inc.
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

"""Command-line application to run a query using user credentials.

You must supply a client secrets file, which would normally be bundled with
your application.
"""

import argparse
import uuid

from google.cloud import bigquery
from google_auth_oauthlib import flow


def run_query(credentials, project, query):
    client = bigquery.Client(project=project, credentials=credentials)
    query_job = client.run_async_query(str(uuid.uuid4()), query)

    query_job.begin()
    query_job.result()  # Wait for the job to complete.

    # Print the results.
    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)


def authenticate_and_query(project, query, launch_browser=True):
    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/bigquery'])

    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()

    run_query(appflow.credentials, project, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--launch-browser',
        help='Use a local server flow to authenticate. ',
        action='store_true')
    parser.add_argument('project', help='Project to use for BigQuery billing.')
    parser.add_argument('query', help='BigQuery SQL Query.')

    args = parser.parse_args()

    authenticate_and_query(
        args.project, args.query, launch_browser=args.launch_browser)
