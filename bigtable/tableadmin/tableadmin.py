#!/usr/bin/env python

# Copyright 2018, Google LLC
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

"""Demonstrates how to connect to Cloud Bigtable and run some basic operations.
#     http://www.apache.org/licenses/LICENSE-2.0
Prerequisites:
- Create a Cloud Bigtable cluster.
  https://cloud.google.com/bigtable/docs/creating-cluster
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials

Operations performed:
- Create a Cloud Bigtable table.
- List tables for a Cloud Bigtable instance.
- Print metadata of the newly created table.
- Create Column Families with different GC rules.
    - GC Rules like: MaxAge, MaxVersions, Union, Intersection and Nested.
- Delete a Bigtable table.
"""

import argparse
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family


def create_table(project_id, instance_id, table_id):
    ''' Create a Bigtable table

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.

    :type table_id: str
    :param table_id: Table id to create table.
    '''

    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    # Check whether table exists in an instance.
    # Create table if it does not exists.
    print('Checking if table {} exists...'.format(table_id))
    if table.exists():
        print('Table {} already exists.'.format(table_id))
    else:
        print('Creating the {} table.'.format(table_id))
        table.create()
        print('Created table {}.'.format(table_id))

    return client, instance, table


def run_table_operations(project_id, instance_id, table_id):
    ''' Create a Bigtable table and perform basic operations on it

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.

    :type table_id: str
    :param table_id: Table id to create table.
    '''

    client, instance, table = create_table(project_id, instance_id, table_id)

    # [START bigtable_list_tables]
    tables = instance.list_tables()
    print('Listing tables in current project...')
    if tables != []:
        for tbl in tables:
            print(tbl.table_id)
    else:
        print('No table exists in current project...')
    # [END bigtable_list_tables]

    # [START bigtable_create_family_gc_max_age]
    print('Creating column family cf1 with with MaxAge GC Rule...')
    # Create a column family with GC policy : maximum age
    # where age = current time minus cell timestamp

    # Define the GC rule to retain data with max age of 5 days
    max_age_rule = column_family.MaxAgeGCRule(datetime.timedelta(days=5))

    column_family1 = table.column_family('cf1', max_age_rule)
    column_family1.create()
    print('Created column family cf1 with MaxAge GC Rule.')
    # [END bigtable_create_family_gc_max_age]

    # [START bigtable_create_family_gc_max_versions]
    print('Creating column family cf2 with max versions GC rule...')
    # Create a column family with GC policy : most recent N versions
    # where 1 = most recent version

    # Define the GC policy to retain only the most recent 2 versions
    max_versions_rule = column_family.MaxVersionsGCRule(2)

    column_family2 = table.column_family('cf2', max_versions_rule)
    column_family2.create()
    print('Created column family cf2 with Max Versions GC Rule.')
    # [END bigtable_create_family_gc_max_versions]

    # [START bigtable_create_family_gc_union]
    print('Creating column family cf3 with union GC rule...')
    # Create a column family with GC policy to drop data that matches
    # at least one condition.
    # Define a GC rule to drop cells older than 5 days or not the
    # most recent version
    union_rule = column_family.GCRuleUnion([
        column_family.MaxAgeGCRule(datetime.timedelta(days=5)),
        column_family.MaxVersionsGCRule(2)])

    column_family3 = table.column_family('cf3', union_rule)
    column_family3.create()
    print('Created column family cf3 with Union GC rule')
    # [END bigtable_create_family_gc_union]

    # [START bigtable_create_family_gc_intersection]
    print('Creating column family cf4 with Intersection GC rule...')
    # Create a column family with GC policy to drop data that matches
    # all conditions
    # GC rule: Drop cells older than 5 days AND older than the most
    # recent 2 versions
    intersection_rule = column_family.GCRuleIntersection([
        column_family.MaxAgeGCRule(datetime.timedelta(days=5)),
        column_family.MaxVersionsGCRule(2)])

    column_family4 = table.column_family('cf4', intersection_rule)
    column_family4.create()
    print('Created column family cf4 with Intersection GC rule.')
    # [END bigtable_create_family_gc_intersection]

    # [START bigtable_create_family_gc_nested]
    print('Creating column family cf5 with a Nested GC rule...')
    # Create a column family with nested GC policies.
    # Create a nested GC rule:
    # Drop cells that are either older than the 10 recent versions
    # OR
    # Drop cells that are older than a month AND older than the
    # 2 recent versions
    rule1 = column_family.MaxVersionsGCRule(10)
    rule2 = column_family.GCRuleIntersection([
        column_family.MaxAgeGCRule(datetime.timedelta(days=30)),
        column_family.MaxVersionsGCRule(2)])

    nested_rule = column_family.GCRuleUnion([rule1, rule2])

    column_family5 = table.column_family('cf5', nested_rule)
    column_family5.create()
    print('Created column family cf5 with a Nested GC rule.')
    # [END bigtable_create_family_gc_nested]

    # [START bigtable_list_column_families]
    print('Printing Column Family and GC Rule for all column families...')
    column_families = table.list_column_families()
    for column_family_name, gc_rule in sorted(column_families.items()):
        print('Column Family:', column_family_name)
        print('GC Rule:')
        print(gc_rule.to_pb())
        # Sample output:
        #         Column Family: cf4
        #         GC Rule:
        #         gc_rule {
        #           intersection {
        #             rules {
        #               max_age {
        #                 seconds: 432000
        #               }
        #             }
        #             rules {
        #               max_num_versions: 2
        #             }
        #           }
        #         }
    # [END bigtable_list_column_families]

    print('Print column family cf1 GC rule before update...')
    print('Column Family: cf1')
    print(column_family1.to_pb())

    # [START bigtable_update_gc_rule]
    print('Updating column family cf1 GC rule...')
    # Update the column family cf1 to update the GC rule
    column_family1 = table.column_family(
        'cf1',
        column_family.MaxVersionsGCRule(1))
    column_family1.update()
    print('Updated column family cf1 GC rule\n')
    # [END bigtable_update_gc_rule]

    print('Print column family cf1 GC rule after update...')
    print('Column Family: cf1')
    print(column_family1.to_pb())

    # [START bigtable_delete_family]
    print('Delete a column family cf2...')
    # Delete a column family
    column_family2.delete()
    print('Column family cf2 deleted successfully.')
    # [END bigtable_delete_family]

    print('execute command "python tableadmin.py delete [project_id] \
            [instance_id] --table [tableName]" to delete the table.')


def delete_table(project_id, instance_id, table_id):
    ''' Delete bigtable.

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.

    :type table_id: str
    :param table_id: Table id to create table.
    '''

    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    # [START bigtable_delete_table]
    # Delete the entire table

    print('Checking if table {} exists...'.format(table_id))
    if table.exists():
        print('Table {} exists.'.format(table_id))
        print('Deleting {} table.'.format(table_id))
        table.delete()
        print('Deleted {} table.'.format(table_id))
    else:
        print('Table {} does not exists.'.format(table_id))
    # [END bigtable_delete_table]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('command',
                        help='run or delete. \
                        Operation to perform on table.')
    parser.add_argument(
        '--table',
        help='Cloud Bigtable Table name.',
        default='Hello-Bigtable')

    parser.add_argument('project_id',
                        help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id',
        help='ID of the Cloud Bigtable instance to connect to.')

    args = parser.parse_args()

    if args.command.lower() == 'run':
        run_table_operations(args.project_id, args.instance_id,
                             args.table)
    elif args.command.lower() == 'delete':
        delete_table(args.project_id, args.instance_id, args.table)
    else:
        print('Command should be either run or delete.\n Use argument -h,\
               --help to show help and exit.')
