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


def write_entry(client, args):
    print('Writing log entry for logger '.format(args.logger_name))
    mylogger = client.logger(args.logger_name)
    # [START write]
    mylogger.log_text(args.entry)
    # [END write]


def list_entries(client, args):
    """Lists all entries for a logger"""
    logger = client.logger(args.logger_name)
    print('Listing all log entries for logger {}'.format(logger.name))
    # [START list]
    entries = []
    while True:
        new_entries, token = client.list_entries(filter_='logName="{}"'.format(
           logger.full_name))
        entries += new_entries
        if token is None:
            break

    for entry in entries:
        timestamp = entry.timestamp.isoformat()
        print('{}: {}'.format
              (timestamp, entry.payload))
    # [END list]
    return entries


def delete_logger(client, args):
    """Deletes a logger and all its entries.

    Note that a deletion can take several minutes to take effect.
    """
    logger = client.logger(args.logger_name)
    print('Deleting all logging entries for {}'.format(logger.name))
    # [START delete]
    logger.delete()
    # [END delete]


def get_client(project_id):
    """Builds an http client authenticated with the service account
    credentials."""
    # [START auth]
    credentials = GoogleCredentials.get_application_default()
    return logging.Client(project=project_id, credentials=credentials)
    # [END auth]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True)
    parser.add_argument(
        '--logger_name', help='Logger name', default='mylogger')

    subparsers = parser.add_subparsers()

    write_parser = subparsers.add_parser('write_entry')
    write_parser.add_argument('entry')
    write_parser.set_defaults(func=write_entry)

    list_parser = subparsers.add_parser('list_entries')
    list_parser.set_defaults(func=list_entries)

    delete_parser = subparsers.add_parser('delete_logger')
    delete_parser.set_defaults(func=delete_logger)

    args = parser.parse_args()
    client = get_client(args.project_id)
    args.func(client, args)
