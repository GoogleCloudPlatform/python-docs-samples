#!/usr/bin/env python

# Copyright 2018 Google Inc.
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

# [START bigtable_quickstart]
import argparse

from google.cloud import bigtable


def main(project_id="project-id", instance_id="instance-id",
         table_id="my-table"):
    # Create a Cloud Bigtable client.
    client = bigtable.Client(project=project_id)

    # Connect to an existing Cloud Bigtable instance.
    instance = client.instance(instance_id)

    # Open an existing table.
    table = instance.table(table_id)

    row_key = 'r1'
    row = table.read_row(row_key.encode('utf-8'))

    column_family_id = 'cf1'
    column_id = 'c1'.encode('utf-8')
    value = row.cells[column_family_id][column_id][0].value.decode('utf-8')

    print('Row key: {}\nData: {}'.format(row_key, value))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        '--table',
        help='Existing table used in the quickstart.',
        default='my-table')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)
# [END bigtable_quickstart]
