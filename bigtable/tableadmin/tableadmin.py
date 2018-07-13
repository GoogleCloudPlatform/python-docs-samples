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


def run_table_operations(project_id, instance_id, table_id):
    ''' Create a Bigtable table and perform basic table operations

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
    print 'Checking if table {} exists...'.format(table_id)
    if exists(instance, table_id):
        print 'Table {} already exists.'.format(table_id)
    else:
        print 'Creating the {} table.'.format(table_id)
        table.create()
        print 'Created table {}.'.format(table_id)

    # [START List existing tables in the instance.]
    tables = instance.list_tables()
    print 'Listing tables in current project...'
    if tables != []:
        for tbl in tables:
            print tbl.table_id
    else:
        print 'No table exists in current project...'
    # [END List existing tables in the instance.]

    # Display name of the table.
    print 'Printing table metadata...'
    print table.table_id

    # [START bigtable_create_family_gc_max_age]
    print 'Creating column family cf1 with with MaxAge GC Rule...'
    # Create a column family with GC policy : maximum age
    # where age = current time minus cell timestamp
    column_family_id1 = 'cf1'
    # Define the GC rule to retain data with max age of 5 days
    max_age = datetime.timedelta(days=5)
    max_age_rule = table.max_age_gc_rule(max_age)
    print 'Created MaxAge GC rule.'

    cf1 = table.column_family(column_family_id1, max_age_rule)
    cf1.create()
    print 'Created column family cf1 with MaxAge GC Rule.'
    # [END bigtable_create_family_gc_max_age]

    # [START bigtable_create_family_gc_max_versions]
    print 'Creating column family cf2 with max versions GC rule...'
    # Create a column family with GC policy : most recent N versions
    # where 1 = most recent version
    column_family_id2 = 'cf2'
    # Define the GC policy to retain only the most recent 2 versions
    max_versions = 2
    max_versions_rule = table.max_versions_gc_rule(max_versions)
    print 'Created Max Versions GC Rule.'

    cf2 = table.column_family(column_family_id2, max_versions_rule)
    cf2 .create()
    print 'Created column family cf2 with Max Versions GC Rule.'
    # [END bigtable_create_family_gc_max_versions]

    # [START bigtable_create_family_gc_union]
    print 'Creating column family cf3 with union GC rule...'
    # Create a column family with GC policy to drop data that matches
    # at least one condition.
    column_family_id3 = 'cf3'
    # GC rule : Drop max age rule OR the most recent version rule.
    union = [max_age_rule, max_versions_rule]
    union_rule = table.gc_rule_union(union)
    print 'Created Union GC Rule.'

    cf3 = table.column_family(column_family_id3, union_rule)
    cf3.create()
    print 'Created column family cf3 with Union GC rule'
    # [END bigtable_create_family_gc_union]

    # [START bigtable_create_family_gc_intersection]
    print 'Creating column family cf4 with Intersection GC rule...'
    # Create a column family with GC policy to drop data that matches
    # all conditions
    column_family_id4 = 'cf4'
    # GC rule: Drop cells older than 5 days AND older than the most
    # recent 2 versions
    intersection = [max_age_rule, max_versions_rule]
    intersection_rule = table.gc_rule_intersection(union)
    print 'Created Intersection GC Rule.'

    cf4 = table.column_family(column_family_id4, intersection_rule)
    cf4.create()
    print 'Created column family cf4 with Intersection GC rule.'
    # [END bigtable_create_family_gc_intersection]

    # [START bigtable_create_family_gc_nested]
    print 'Creating column family cf5 with a Nested GC rule...'
    # Create a column family with nested GC policys.
    # Create a nested GC rule:
    # Drop cells that are either older than the 10 recent versions
    # OR
    # Drop cells that are older than a month AND older than the
    # 2 recent versions
    column_family_id5 = 'cf5'
    # Drop cells that are either older than the 10 recent versions
    max_versions_rule1 = table.max_versions_gc_rule(10)

    # Drop cells that are older than a month AND older than
    # the 2 recent versions
    max_age = datetime.timedelta(days=30)
    max_age_rule = table.max_age_gc_rule(max_age)
    max_versions_rule2 = table.max_versions_gc_rule(2)
    intersection = [max_age_rule, max_versions_rule2]
    intersection_rule = table.gc_rule_intersection(intersection)

    # This nesting is done with union rule since it is OR between
    # the selected rules.
    nest = [max_versions_rule1, intersection_rule]
    nested_rule = table.gc_rule_union(nest)
    print 'Created Nested GC Rule.'

    cf5 = table.column_family(column_family_id5, nested_rule)
    cf5.create()
    print 'Created column family cf5 with a Nested GC rule.'
    # [END bigtable_create_family_gc_nested]

    # [START bigtable_list_column_families]
    print 'Printing Column Family and GC Rule for all column families...'
    column_families = table.list_column_families()
    for column_family, gc_rule in sorted(column_families.items()):
        print "Column Family:", column_family
        print "GC Rule:"
        print gc_rule.to_pb()
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

    # [START bigtable_update_gc_rule]
    print 'Updating column family cf1 GC rule...'
    # Update the column family cf1 to update the GC rule
    max_versions = 1
    max_versions_rule = table.max_versions_gc_rule(max_versions)
    # Create a reference to the column family with GC rule
    cf1 = table.column_family(column_family_id1, max_versions_rule)
    cf1.update()
    print 'Updated column family cf1 GC rule'
    # [END bigtable_update_gc_rule]

    # [START bigtable_family_get_gc_rule]
    print 'Print updated column family cf1 GC rule...'
    print 'Column Family:', column_family_id1
    print 'GC Rule:'
    print cf1.to_pb()
    # [END bigtable_family_get_gc_rule]

    # [START bigtable_delete_family]
    print 'Delete a column family cf2...'
    # Delete a column family
    cf2.delete()
    print 'Column family cf2 deleted successfully.'
    # [END bigtable_delete_family]

    print 'execute command python tableadmin.py delete [project_id] \
            [instance_id] --table [tableName] to delete the table.'


def exists(instance_obj, table_id):
    """ Check whether table exists or not.

        .. note::

            This is temporary function as code for this is under development.
            Once complete, this function would be removed.

    :type instance_obj: Instance Class.
    :param instance_obj: Instance object.

    :type table_id: str
    :param table_id: Table id to create table.
    Returns bool
    """
    for table in instance_obj.list_tables():
        if table_id == table.table_id:
            return True
    return False


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

    print 'Checking if table {} exists...'.format(table_id)
    if exists(instance, table_id):
        print 'Table {} exists.'.format(table_id)
        print 'Deleting {} table.'.format(table_id)
        table.delete()
        print 'Deleted {} table.'.format(table_id)
    else:
        print 'Table {} does not exists.'.format(table_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('command',
                        help='run or delete. Operation to perform on table.')
    parser.add_argument(
        '--table',
        help='Cloud Bigtable Table name.',
        default='Hello-Bigtable')

    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')

    args = parser.parse_args()

    if args.command.lower() == 'run':
        run_table_operations(args.project_id, args.instance_id, args.table)
    elif args.command.lower() == 'delete':
        delete_table(args.project_id, args.instance_id, args.table)
    else:
        print 'Command should be either run or delete.\n Use argument -h, \
               --help to show help and exit.'
