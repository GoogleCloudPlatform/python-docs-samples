# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
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
"""

import datetime
import argparse
from google.cloud import bigtable

def run_table_operations(project_id, instance_id, table_id):
    ''' Create bigtable and perform different operations on it.
        :project_id: Project id of the client
        :instance_id: Instance of the client
        :table_id: Table id to create table.
    '''
    
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    
    table_exists = exists()
    print('Checking if table {} exists...'.format(table_id))
    try:            
        
        if table_exists:
            print('Table {} already exists.'.format(table_id))
    except :
        print('Error checking table exists.'.format(table_id))
    
    if not table_exists:
        print('Creating table {}.'.format(table_id))    
        try:            
            table.create()
        except :
            print('Error creating table {}.'.format(table_id))
        else:
            print('Created table {}.'.format(table_id))
            
    try:
        tables = instance.list_tables()  #table.get_tables()
        
    except:
        print('Error listing tables.')
        
    print('Listing tables in current project...')
    if tables != []:
        for t in tables:
            print t.name
    else:
        print('No table exists in current project...')
    
        
    print('Printing table metadata...')
    try:
        print(table.name)
    except :
        print('Error retrieving table metadata.')
    
    return 1
    print('Creating column family cf1 with with MaxAge GC Rule...')
    # [START bigtable_create_family_gc_max_age]
    # Create a column family with GC policy : maximum age
    # where age = current time minus cell timestamp
    column_family_id1 = 'cf1'
    try:
        # Define the GC rule to retain data with max age of 5 days
        max_age = datetime.timedelta(days=5)
        max_age_rule = table.max_age_gc_rule(max_age)
        print('Created column MaxAge GC rule')
    except:
        print('Error creating MaxAge GC Rule.')
    
    try:
        cf1 = table.column_family(column_family_id1, max_age_rule)
        cf1.create()
        print('Created column family cf1 with MaxAge GC Rule.')
    except:
        print('Error creating column family with MaxAge GC Rule.')
    # [End bigtable_create_family_gc_max_age]
    
    
    print('Creating column family cf2 with max versions GC rule...')
    # [START bigtable_create_family_gc_max_versions]
    # Create a column family with GC policy : most recent N versions
    # where 1 = most recent version
    column_family_id2 = 'cf2'
    try:
        # Define the GC policy to retain only the most recent 2 versions
        max_versions = 2
        max_versions_rule = table.max_versions_gc_rule(max_versions)
        print('Created column Max Versions GC Rule.')
    except:
        print('Error creating Max Versions GC Rule.')
    
    try:
        cf2 = table.column_family(column_family_id2, max_versions_rule)
        cf2 .create()
        print('Created column family cf2 with Max Versions GC Rule.')
    except:
        print('Error creating column family with Max Versions GC Rule.')
    # [END bigtable_create_family_gc_max_versions]  
    
    
    print('Creating column family cf3 with union GC rule...')
    # [START bigtable_create_family_gc_union]
    # Create a column family with GC policy to drop data that matches at least one condition.
    column_family_id3 = 'cf3'
    try:
        # GC rule : Drop max age rule OR the most recent version rule.
        union = [max_age_rule, max_versions_rule]    
        union_rule = table.gc_rule_union(union)
        print('Created column Union GC Rule.')
    except:
        print('Error creating Union GC Rule.')
     
    try:
        cf3 = table.column_family(column_family_id3, union_rule)
        cf3.create()
        print('Created column family cf3 with Union GC rule')
    except:
        print('Error creating column family with Union GC rule')
    # [END bigtable_create_family_gc_union]
    
    
    
    print('Creating column family cf4 with Intersection GC rule...')
    # [START bigtable_create_family_gc_intersection]
    # Create a column family with GC policy to drop data that matches all conditions
    column_family_id4 = 'cf4'
    
    try:
        # GC rule: Drop cells older than 5 days AND older than the most recent 2 versions
        intersection = [max_age_rule, max_versions_rule]    
        intersection_rule = table.gc_rule_intersection(union)
        print('Created column Intersection GC Rule.')
    except:
        print('Error creating Intersection GC Rule.')
        
    try:
        cf4 = table.column_family(column_family_id4, intersection_rule)
        cf4.create()
        print('Created column family cf4 with Intersection GC rule.')
    except:
        print('Error creating column family with Intersection GC rule.')
    # [END bigtable_create_family_gc_intersection]
    
    
    print('Creating column family cf5 with a Nested GC rule...')
    # [START bigtable_create_family_gc_nested]
    # Create a column family with nested GC policys.
    
    # Create a nested GC rule:
    # Drop cells that are either older than the 10 recent versions
    # OR
    # Drop cells that are older than a month AND older than the 2 recent versions
    column_family_id5 = 'cf5'
    try:
        # Drop cells that are either older than the 10 recent versions
        max_versions_rule1 = table.max_versions_gc_rule(10)
        
        # Drop cells that are older than a month AND older than the 2 recent versions
        max_age = datetime.timedelta(days=30)
        max_age_rule = table.max_age_gc_rule(max_age)
        max_versions_rule2 = table.max_versions_gc_rule(2)
        intersection = [max_age_rule, max_versions_rule2]
        intersection_rule = table.gc_rule_intersection(intersection)
        
        # This nesting is done with union rule since it is OR between the selected rules. 
        nest = [max_versions_rule1, intersection_rule]
        nested_rule = table.gc_rule_union(nest)
        print('Created column Nested GC Rule.')
    except:
        print('Error creating Nested GC Rule.')
        
    try:
        cf5 = table.column_family(column_family_id5, nested_rule)
        cf5.create()
        print('Created column family cf5 with a Nested GC rule.')
    except:
        print('Error creating column family with a Nested GC rule.')
    # [END bigtable_create_family_gc_nested]
    
    
    print('Printing ID and GC Rule for all column families...')
    cf = table.list_column_families()
    column_families = [key for key,val in cf.items()]
    for cf,gc_rule in sorted(cf.items()):
        print "Column Family:", cf
        print "GC Rule:"
        print list_gc_rules(gc_rule)
        
def list_gc_rules(column_family):
    return column_family.gc_rule.to_pb()

def exists():
    return False 
    
def delete_table(project_id, instance_id, table_id):
    ''' Delete bigtable.
        :project_id: Project id of the client
        :instance_id: Instance of the client
        :table_id: Table id to create table.
    '''
    
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    table_exists = False
    
    print('Checking if {} table exists...'.format(table_id))
    try:            
        table_exists = table.exists()
    except :
        print('Error checking table exists.'.format(table_id))
    
    #if not table_exists:
    if False:
        print('Table {} does not exists.'.format(table_id))
    else:
        try:
            print('Deleting {} table.'.format(table_id))
            table.delete()
        except:
            print('Error deleting {} table.'.format(table_id))
        else: 
            print('Deleted {} table.'.format(table_id))
    

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
        delete_table(args.project_id, args.instance_id, args.table)
    elif args.command.lower() == 'delete':
        delete_table(args.project_id, args.instance_id, args.table)
    else:
        print ('Command should be either run or delete.\n Use argument -h, --help to show help and exit.')
        
    
