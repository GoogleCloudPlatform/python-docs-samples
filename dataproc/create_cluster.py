#!/usr/bin/env python

# Copyright 2019 Google LLC
#
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


def create_cluster(project_id, region, cluster_name):
    # [START dataproc_create_cluster]
    from google.cloud import dataproc_v1 as dataproc

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # region = 'YOUR_CLUSTER_REGION'
    # cluster_name = 'YOUR_CLUSTER_NAME'

    # Create a client with the endpoint set to the desired cluster region
    client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    # Create the cluster config
    cluster = {
        'project_id': project_id,
        'cluster_name': cluster_name,
        'config': {
            'master_config': {
                'num_instances': 1,
                'machine_type_uri': 'n1-standard-1'
            },
            'worker_config': {
                'num_instances': 2,
                'machine_type_uri': 'n1-standard-1'
            }
        }
    }

    # Create the cluster
    operation = client.create_cluster(project_id, region, cluster)
    result = operation.result()

    # Output a success message
    print('Cluster created successfully: {}'.format(result.cluster_name))
    # [END dataproc_create_cluster]
