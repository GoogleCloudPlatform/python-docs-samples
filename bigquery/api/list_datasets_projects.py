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

"""Command-line application to list all projects and datasets in BigQuery.

This sample is used on this page:

    https://cloud.google.com/bigquery/docs/managing_jobs_datasets_projects

For more information, see the README.md under /bigquery.
"""

import argparse
from pprint import pprint

import googleapiclient.discovery
from six.moves.urllib.error import HTTPError


# [START list_datasets]
def list_datasets(bigquery, project):
    try:
        datasets = bigquery.datasets()
        list_reply = datasets.list(projectId=project).execute()
        print('Dataset list:')
        pprint(list_reply)

    except HTTPError as err:
        print('Error in list_datasets: %s' % err.content)
        raise err
# [END list_datasets]


# [START list_projects]
def list_projects(bigquery):
    try:
        projects = bigquery.projects()
        list_reply = projects.list().execute()

        print('Project list:')
        pprint(list_reply)

    except HTTPError as err:
        print('Error in list_projects: %s' % err.content)
        raise err
# [END list_projects]


def main(project_id):
    # Construct the service object for interacting with the BigQuery API.
    bigquery = googleapiclient.discovery.build('bigquery', 'v2')

    list_datasets(bigquery, project_id)
    list_projects(bigquery)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='the project id to list.')

    args = parser.parse_args()

    main(args.project_id)
