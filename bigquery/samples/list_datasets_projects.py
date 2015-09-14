# -*- coding: utf-8 -*-
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
#
"""Command-line skeleton application for BigQuery API.

This is the sample for this page:

    https://cloud.google.com/bigquery/docs/managing_jobs_datasets_projects

In order to run it, your environment must be setup with authentication
information [1]. If you're running it in your local development environment and
you have the Google Cloud SDK [2] installed, you can do this easily by running:

    $ gcloud auth login

Usage:

    $ python list_datasets_projects.py <project-id>

where <project-id> is the id of the developers console [3] project you'd like
to list the bigquery datasets and projects for.

[1] https://developers.google.com/identity/protocols/\
    application-default-credentials#howtheywork
[2] https://cloud.google.com/sdk/
[3] https://console.developers.google.com

For more information on the BigQuery API you can visit:

  https://developers.google.com/bigquery/docs/overview

For more information on the BigQuery API Python library surface you
can visit:

  https://developers.google.com/resources/api-libraries/documentation/
  bigquery/v2/python/latest/

For information on the Python Client Library visit:

  https://developers.google.com/api-client-library/python/start/get_started
"""

import argparse
from pprint import pprint

from apiclient import discovery
from oauth2client.client import GoogleCredentials
from six.moves.urllib.error import HTTPError


# [START list_datasets]
def list_datasets(service, project):
    try:
        datasets = service.datasets()
        list_reply = datasets.list(projectId=project).execute()
        print('Dataset list:')
        pprint(list_reply)

    except HTTPError as err:
        print('Error in list_datasets: %s' % err.content)
# [END list_datasets]


# [START list_projects]
def list_projects(service):
    try:
        # Start training on a data set
        projects = service.projects()
        list_reply = projects.list().execute()

        print('Project list:')
        pprint(list_reply)

    except HTTPError as err:
        print('Error in list_projects: %s' % err.content)
# [END list_projects]


def main(project_id):
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    service = discovery.build('bigquery', 'v2', credentials=credentials)

    list_datasets(service, project_id)
    list_projects(service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Lists BigQuery datasets and projects.')
    parser.add_argument('project_id', help='the project id to list.')

    args = parser.parse_args()

    main(args.project_id)
