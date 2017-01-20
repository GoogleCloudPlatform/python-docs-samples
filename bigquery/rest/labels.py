#!/usr/bin/env python

# Copyright 2016, Google, Inc.
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

"""Application to add or modify a label on a BigQuery dataset or table."""

import argparse

import google.auth
import google.auth.transport.requests


def label_dataset(dataset_id, label_key, label_value, project_id=None):
    """Add or modify a label on a dataset."""
    # Authenticate requests using Google Application Default credentials.
    credentials, default_project_id = google.auth.default(
            scopes=['https://www.googleapis.com/auth/bigquery'])
    session = google.auth.transport.requests.AuthorizedSession(credentials)

    if project_id is None:
        project_id = default_project_id

    # Send a PATCH request to add or modify a label.
    url_format = (
        'https://www.googleapis.com/bigquery/v2/'
        'projects/{project_id}/datasets/{dataset_id}')
    response = session.patch(
        url_format.format(project_id=project_id, dataset_id=dataset_id),
        params={'fields': 'labels'},
        json={
            'labels': {
                label_key: label_value,
            }
        })

    # Check the response for errors.
    response.raise_for_status()

    # Print the new label value from the response.
    labels = response.json()['labels']
    print(
        'Updated label "{}" with value "{}"'.format(
            label_key,
            labels[label_key]))


def label_table(dataset_id, table_id, label_key, label_value, project_id=None):
    """Add or modify a label on a table."""
    # Authenticate requests using Google Application Default credentials.
    credentials, default_project_id = google.auth.default(
            scopes=['https://www.googleapis.com/auth/bigquery'])
    session = google.auth.transport.requests.AuthorizedSession(credentials)

    if project_id is None:
        project_id = default_project_id

    # Send a PATCH request to add or modify a label.
    url_format = (
        'https://www.googleapis.com/bigquery/v2/'
        'projects/{project_id}/datasets/{dataset_id}/tables/{table_id}')
    response = session.patch(
        url_format.format(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id),
        params={'fields': 'labels'},
        json={
            'labels': {
                label_key: label_value,
            }
        })

    # Check the response for errors.
    response.raise_for_status()

    # Print the new label value from the response.
    labels = response.json()['labels']
    print(
        'Updated label "{}" with value "{}"'.format(
            label_key,
            labels[label_key]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_id', help='BigQuery dataset ID.')
    parser.add_argument('label_key', help='Key for new/modified label.')
    parser.add_argument('label_value', help='Value for new/modified label.')
    parser.add_argument(
        '--project_id',
        help=(
            'Google Cloud project ID. '
            'If not set, uses a default value from the environment.'),
        default=None)
    parser.add_argument(
        '--table_id',
        help=(
            'BigQuery table ID. '
            'If present, a label is added to the specified table instead of '
            'the dataset.'),
        default=None)

    args = parser.parse_args()

    if args.table_id is None:
        label_dataset(
            args.dataset_id,
            args.label_key,
            args.label_value,
            project_id=args.project_id)
    else:
        label_table(
            args.dataset_id,
            args.table_id,
            args.label_key,
            args.label_value,
            project_id=args.project_id)
