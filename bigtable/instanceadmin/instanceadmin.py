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
- Create a Cloud Bigtable project.
  https://cloud.google.com/bigtable/docs/
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials

Operations performed:
- Create a Cloud Bigtable Instance.
- List Instance for a Cloud Bigtable.
- Delete a Bigtable Instance.
- Create a Bigtable Cluster.
- List Bigtable clusters.
- Delete a Bigtable Cluster.
"""

import argparse
from google.cloud import bigtable


def run_instance_operations(project_id, instance_id, cluster_id):
    client = bigtable.Client(project=project_id, admin=True)
    location_id = 'us-central1-f'
    serve_nodes = 3
    production = 1
    instance = client.instance(instance_id, instance_type=production)
    
    # [START bigtable_check_instance_exists]
    if not instance.exists():
        print 'Instance does not exists'
    # [END bigtable_check_instance_exists]

    # [START bigtable_create_prod_instance]
    print '\nCreating a Instance'
    # Set options to create an Instance

    # Create instance with given options
    instance.create(location_id=location_id, serve_nodes=serve_nodes)

    print '\nCreated instance: {}'.format(instance_id)
    # [END bigtable_create_prod_instance]

    # [START bigtable_list_instances]
    print '\nListing Instances:'
    #instance_list =  client.list_instances()
    for instance_local in client.list_instances()[0]:
        print instance_local.instance_id
    # [END bigtable_list_instances]

    # [START bigtable_get_instance]
    print '\nName of instance: {}'.format(instance_id)
    # [END bigtable_get_instance]

    # [START bigtable_get_clusters]
    print '\nListing Clusters...'
    for cluster in instance.list_clusters()[0]:
        print cluster.cluster_id
    # [END bigtable_get_clusters]

def create_dev_instance(project_id, instance_id):
    ''' Creates a Development instance with the name "hdd-instance"
        location us-central1-f
        Cluster nodes should not be set while creating Development
        Instance

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.
    '''

    client = bigtable.Client(project=project_id, admin=True)

    # [START bigtable_create_dev_instance]
    print '\nCreating a DEVELOPMENT Instance'
    # Set options to create an Instance
    location_id = 'us-central1-f'
    development = 2

    # Create instance with given options
    instance = client.instance(instance_id, instance_type=development)

    # Create development instance with given options
    instance.create(location_id=location_id)
    print 'Created development instance: {}'.format(instance_id)
    # [END bigtable_create_dev_instance]


def delete_instance(project_id, instance_id):
    ''' Delete the Instance

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.
    '''

    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    #instance.create()
    # [START bigtable_delete_instance]
    print '\nDeleting Instance'
    if not instance.exists():
        print 'Instance does not exists', instance_id
    else:
        instance.delete()
        print 'Deleted Instance: {}'.format(instance_id)
    # [END bigtable_delete_instance]


def add_cluster(project_id, instance_id, cluster_id):
    ''' Add Cluster

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.

    :type cluster_id: str
    :param cluster_id: Cluster id.
    '''
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)

    location_id = 'us-central2-f'
    serve_nodes = 3

    if not instance.exists():
        print 'Instance does not exists.'
    else:
        print '\nAdding Cluster to Instance {}'.format(instance_id)
        # [START bigtable_create_cluster]
        print '\nListing Clusters...'
        for cluster in instance.list_clusters()[0]:
            print cluster.cluster_id
        cluster = instance.cluster(cluster_id, location_id=location_id, serve_nodes=serve_nodes)
        print dir(cluster), cluster.location_id, cluster.location_id
        cluster.create()
        print 'Cluster created: {}'.format(cluster_id)
        # [END bigtable_create_cluster]


def delete_cluster(project_id, instance_id, cluster_id):
    ''' Delete the cluster

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.

    :type cluster_id: str
    :param cluster_id: Cluster id.
    '''

    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    cluster = instance.cluster(cluster_id)

    # [START bigtable_delete_cluster]
    print '\nDeleting Cluster'
    cluster.delete()
    print 'Cluster deleted: {}'.format(cluster)
    # [END bigtable_delete_cluster]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('command',
                        help='run, dev-instance, del-instance, \
                            add-cluster or del-cluster. \
                            Operation to perform on Instance.')
    parser.add_argument('project_id', \
                help='Your Cloud Platform project ID.')
    parser.add_argument('instance_id', \
                help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument('cluster_id', \
                help='ID of the Cloud Bigtable cluster to connect to.')

    args = parser.parse_args()

    if args.command.lower() == 'run':
        run_instance_operations(args.project_id, args.instance_id, args.cluster_id)
    elif args.command.lower() == 'dev-instance':
        create_dev_instance(args.project_id, args.instance_id)
    elif args.command.lower() == 'del-instance':
        delete_instance(args.project_id, args.instance_id)
    elif args.command.lower() == 'add-cluster':
        add_cluster(args.project_id, args.instance_id, args.cluster_id)
    elif args.command.lower() == 'del-cluster':
        delete_cluster(args.project_id, args.instance_id, args.cluster_id)
    else:
        print 'Command should be either run \n Use argument -h, \
               --help to show help and exit.'
