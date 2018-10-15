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
- Delete a Cloud Bigtable Instance.
- Create a Cloud Bigtable Cluster.
- List Cloud Bigtable Clusters.
- Delete a Cloud Bigtable Cluster.
"""

import argparse

from google.cloud import bigtable
from google.cloud.bigtable import enums


def run_instance_operations(project_id, instance_id):
    ''' Check Instance exists.
        Creates a Production instance with default Cluster.
        List instances in a project.
        List clusters in an instance.

    :type project_id: str
    :param project_id: Project id of the client.

    :type instance_id: str
    :param instance_id: Instance of the client.
    '''
    client = bigtable.Client(project=project_id, admin=True)
    location_id = 'us-central1-f'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}
    instance = client.instance(instance_id, instance_type=production,
                               labels=labels)

    # [START bigtable_check_instance_exists]
    if not instance.exists():
        print('Instance {} does not exists.'.format(instance_id))
    else:
        print('Instance {} already exists.'.format(instance_id))
    # [END bigtable_check_instance_exists]

    # [START bigtable_create_prod_instance]
    cluster = instance.cluster("ssd-cluster1", location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    if not instance.exists():
        print('\nCreating an Instance')
        # Create instance with given options
        instance.create(clusters=[cluster])
        print('\nCreated instance: {}'.format(instance_id))
    # [END bigtable_create_prod_instance]

    # [START bigtable_list_instances]
    print('\nListing Instances:')
    for instance_local in client.list_instances()[0]:
        print(instance_local.instance_id)
    # [END bigtable_list_instances]

    # [START bigtable_get_instance]
    print('\nName of instance:{}\nLabels:{}'.format(instance.display_name,
                                                    instance.labels))
    # [END bigtable_get_instance]

    # [START bigtable_get_clusters]
    print('\nListing Clusters...')
    for cluster in instance.list_clusters()[0]:
        print(cluster.cluster_id)
    # [END bigtable_get_clusters]


def create_dev_instance(project_id, instance_id, cluster_id):
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
    print('\nCreating a DEVELOPMENT Instance')
    # Set options to create an Instance
    location_id = 'us-central1-f'
    development = enums.Instance.Type.DEVELOPMENT
    storage_type = enums.StorageType.HDD
    labels = {'dev-label': 'dev-label'}

    # Create instance with given options
    instance = client.instance(instance_id, instance_type=development,
                               labels=labels)
    cluster = instance.cluster(cluster_id, location_id=location_id,
                               default_storage_type=storage_type)

    # Create development instance with given options
    if not instance.exists():
        instance.create(clusters=[cluster])
        print('Created development instance: {}'.format(instance_id))
    else:
        print('Instance {} already exists.'.format(instance_id))

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
    # [START bigtable_delete_instance]
    print('\nDeleting Instance')
    if not instance.exists():
        print('Instance {} does not exists.'.format(instance_id))
    else:
        instance.delete()
        print('Deleted Instance: {}'.format(instance_id))
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

    location_id = 'us-central1-a'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD

    if not instance.exists():
        print('Instance {} does not exists.'.format(instance_id))
    else:
        print('\nAdding Cluster to Instance {}'.format(instance_id))
        # [START bigtable_create_cluster]
        print('\nListing Clusters...')
        for cluster in instance.list_clusters()[0]:
            print(cluster.cluster_id)
        cluster = instance.cluster(cluster_id, location_id=location_id,
                                   serve_nodes=serve_nodes,
                                   default_storage_type=storage_type)
        if cluster.exists():
            print(
                '\nCluster not created, as {} already exists.'.
                format(cluster_id)
            )
        else:
            cluster.create()
            print('\nCluster created: {}'.format(cluster_id))
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
    print('\nDeleting Cluster')
    if cluster.exists():
        cluster.delete()
        print('Cluster deleted: {}'.format(cluster_id))
    else:
        print('\nCluster {} does not exist.'.format(cluster_id))

    # [END bigtable_delete_cluster]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('command',
                        help='run, dev-instance, del-instance, \
                        add-cluster or del-cluster. \
                        Operation to perform on Instance.')
    parser.add_argument('project_id',
                        help='Your Cloud Platform project ID.')
    parser.add_argument('instance_id',
                        help='ID of the Cloud Bigtable instance to \
                        connect to.')
    parser.add_argument('cluster_id',
                        help='ID of the Cloud Bigtable cluster to \
                        connect to.')

    args = parser.parse_args()

    if args.command.lower() == 'run':
        run_instance_operations(args.project_id, args.instance_id)
    elif args.command.lower() == 'dev-instance':
        create_dev_instance(args.project_id, args.instance_id,
                            args.cluster_id)
    elif args.command.lower() == 'del-instance':
        delete_instance(args.project_id, args.instance_id)
    elif args.command.lower() == 'add-cluster':
        add_cluster(args.project_id, args.instance_id, args.cluster_id)
    elif args.command.lower() == 'del-cluster':
        delete_cluster(args.project_id, args.instance_id, args.cluster_id)
    else:
        print('Command should be either run \n Use argument -h, \
               --help to show help and exit.')
