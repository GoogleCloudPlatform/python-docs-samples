#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application that demonstrates using BigQuery with credentials
obtained from an installed app.

This sample is used on this page:

    https://cloud.google.com/bigquery/authentication

For more information, see the README.md under /bigquery.
"""
# [START all]

import argparse
import pprint

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from oauth2client import tools
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

SCOPES = ['https://www.googleapis.com/auth/bigquery']
# Update with the full path to your client secrets json file.
CLIENT_SECRETS = 'client_secrets.json'


def main(args):
    storage = Storage('credentials.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(
            CLIENT_SECRETS, scope=SCOPES)
        # run_flow will prompt the user to authorize the application's
        # access to BigQuery and return the credentials.
        credentials = tools.run_flow(flow, storage, args)

    # Create a BigQuery client using the credentials.
    bigquery_service = googleapiclient.discovery.build(
        'bigquery', 'v2', credentials=credentials)

    # List all datasets in BigQuery
    try:
        datasets = bigquery_service.datasets()
        listReply = datasets.list(projectId=args.project_id).execute()
        print('Dataset list:')
        pprint.pprint(listReply)

    except HttpError as err:
        print('Error in listDatasets:')
        pprint.pprint(err.content)

    except AccessTokenRefreshError:
        print('Credentials have been revoked or expired, please re-run'
              'the application to re-authorize')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Use oauth2client's argparse as a base, so that the flags needed
        # for run_flow are available.
        parents=[tools.argparser])
    parser.add_argument(
        'project_id', help='Your Google Cloud Project ID.')
    args = parser.parse_args()
    main(args)
# [END all]
