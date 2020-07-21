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


def main(project, launch_browser=True):
    # [START bigquery_auth_user_flow]
    from google_auth_oauthlib import flow

    # TODO: Uncomment the line below to set the `launch_browser` variable.
    # launch_browser = True
    #
    # The `launch_browser` boolean variable indicates if a local server is used
    # as the callback URL in the auth flow. A value of `True` is recommended,
    # but a local server does not work if accessing the application remotely,
    # such as over SSH or from a remote Jupyter notebook.

    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()

    credentials = appflow.credentials
    # [END bigquery_auth_user_flow]

    # [START bigquery_auth_user_query]
    from google.cloud import bigquery

    # TODO: Uncomment the line below to set the `project` variable.
    # project = 'user-project-id'
    #
    # The `project` variable defines the project to be billed for query
    # processing. The user must have the bigquery.jobs.create permission on
    # this project to run a query. See:
    # https://cloud.google.com/bigquery/docs/access-control#permissions

    client = bigquery.Client(project=project, credentials=credentials)

    query_string = """SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE name = 'William'
    GROUP BY name;
    """
    query_job = client.query(query_string)

    # Print the results.
    for row in query_job.result():  # Wait for the job to complete.
        print("{}: {}".format(row["name"], row["total"]))
    # [END bigquery_auth_user_query]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--launch-browser",
        help="Use a local server flow to authenticate. ",
        action="store_true",
    )
    parser.add_argument("project", help="Project to use for BigQuery billing.")

    args = parser.parse_args()

    main(args.project, launch_browser=args.launch_browser)
