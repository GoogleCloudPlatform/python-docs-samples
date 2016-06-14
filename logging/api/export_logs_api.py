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

import argparse

from gcloud import logging
from oauth2client.client import GoogleCredentials

FILTER = 'logName="projects/{}/logs/syslog" AND severity>=ERROR'
DESTINATION = 'storage.googleapis.com/{}'


def create_sink_if_not_exists(client, args):
    # [START create]
    sink = client.sink(
        args.sink_name,
        FILTER.format(args.project_id),
        DESTINATION.format(args.destination_bucket))

    if not sink.exists():
        sink.create()
        print('Created sink {}'.format(sink.name))
    # [END create]
    return sink


def list_sinks(client, args):
    print('Listing sinks available')

    # [START list]
    sinks = []
    token = None
    while True:
        new_sinks, token = client.list_sinks(page_token=token)
        sinks += new_sinks
        if token is None:
            break

    for sink in sinks:
        print('{}: {}'.format(sink.name, sink.destination))
    # [END list]

    return sinks


def update_sink(client, args):
    """Changes the filter of a sink.

     The filter is used to determine which log statements match this sink and
     will be exported to the destination.
    """
    # Removes the robot in textPayload part of filter
    # [START update]
    sink = client.sink(
        args.sink_name,
        FILTER.format(args.project_id),
        DESTINATION.format(args.destination_bucket))

    sink.filter = ('logName="projects/{}/logs/syslog" '
                   'AND severity>= INFO'.format(sink.project))
    print('Updated sink {}'.format(sink.name))
    sink.update()
    # [END update]


def delete_sink(client, args):
    """Deletes a sink"""
    # [START delete]
    sink = client.sink(
        args.sink_name,
        FILTER.format(args.project_id),
        DESTINATION.format(args.destination_bucket))
    sink.delete()
    # [END delete]
    print('Deleted sink {}'.format(sink.name))


def get_client(project_id):
    """Builds an http client authenticated with the service account
    credentials."""
    credentials = GoogleCredentials.get_application_default()
    return logging.Client(project=project_id, credentials=credentials)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True,)

    parser.add_argument(
        '--sink_name', help='Output bucket to direct sink to',
        default="mysink")

    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create_sink')
    create_parser.set_defaults(func=create_sink_if_not_exists)
    create_parser.add_argument(
        '--destination_bucket', help='Output bucket to direct sink to',
        required=True)

    list_parser = subparsers.add_parser('list_sinks')
    list_parser.set_defaults(func=list_sinks)

    update_parser = subparsers.add_parser('update_sink')
    update_parser.set_defaults(func=update_sink)
    update_parser.add_argument(
        '--destination_bucket', help='Output bucket to direct sink to',
        required=True)

    delete_parser = subparsers.add_parser('delete_sink')
    delete_parser.add_argument(
        '--destination_bucket', help='Output bucket to direct sink to',
        required=True)
    delete_parser.set_defaults(func=delete_sink)

    args = parser.parse_args()
    client = get_client(args.project_id)
    args.func(client, args)
