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

from google.cloud import logging


def list_sinks():
    """Lists all sinks."""
    logging_client = logging.Client()

    sinks = list(logging_client.list_sinks())

    if not sinks:
        print('No sinks.')

    for sink in sinks:
        print('{}: {} -> {}'.format(sink.name, sink.filter_, sink.destination))


def create_sink(sink_name, destination_bucket, filter_):
    """Creates a sink to export logs to the given Cloud Storage bucket.

    The filter determines which logs this sink matches and will be exported
    to the destination. For example a filter of 'severity>=INFO' will send
    all logs that have a severity of INFO or greater to the destination.
    See https://cloud.google.com/logging/docs/view/advanced_filters for more
    filter information.
    """
    logging_client = logging.Client()

    # The destination can be a Cloud Storage bucket, a Cloud Pub/Sub topic,
    # or a BigQuery dataset. In this case, it is a Cloud Storage Bucket.
    # See https://cloud.google.com/logging/docs/api/tasks/exporting-logs for
    # information on the destination format.
    destination = 'storage.googleapis.com/{bucket}'.format(
        bucket=destination_bucket)

    sink = logging_client.sink(
        sink_name,
        filter_,
        destination)

    if sink.exists():
        print('Sink {} already exists.'.format(sink.name))
        return

    sink.create()
    print('Created sink {}'.format(sink.name))


def update_sink(sink_name, filter_):
    """Changes a sink's filter.

    The filter determines which logs this sink matches and will be exported
    to the destination. For example a filter of 'severity>=INFO' will send
    all logs that have a severity of INFO or greater to the destination.
    See https://cloud.google.com/logging/docs/view/advanced_filters for more
    filter information.
    """
    logging_client = logging.Client()
    sink = logging_client.sink(sink_name)

    sink.reload()

    sink.filter_ = filter_
    print('Updated sink {}'.format(sink.name))
    sink.update()
    # [END update]


def delete_sink(sink_name):
    """Deletes a sink."""
    logging_client = logging.Client()
    sink = logging_client.sink(sink_name)

    sink.delete()

    print('Deleted sink {}'.format(sink.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help=list_sinks.__doc__)

    create_parser = subparsers.add_parser('create', help=list_sinks.__doc__)
    create_parser.add_argument(
        'sink_name',
        help='Name of the log export sink.')
    create_parser.add_argument(
        'destination_bucket',
        help='Cloud Storage bucket where logs will be exported.')
    create_parser.add_argument(
        'filter',
        help='The filter used to match logs.')

    update_parser = subparsers.add_parser('update', help=update_sink.__doc__)
    update_parser.add_argument(
        'sink_name',
        help='Name of the log export sink.')
    update_parser.add_argument(
        'filter',
        help='The filter used to match logs.')

    delete_parser = subparsers.add_parser('delete', help=delete_sink.__doc__)
    delete_parser.add_argument(
        'sink_name',
        help='Name of the log export sink.')

    args = parser.parse_args()

    if args.command == 'list':
        list_sinks()
    elif args.command == 'create':
        create_sink(args.sink_name, args.destination_bucket, args.filter)
    elif args.command == 'update':
        update_sink(args.sink_name, args.filter)
    elif args.command == 'delete':
        delete_sink(args.sink_name)
