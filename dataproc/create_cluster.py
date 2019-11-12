#!/usr/bin/env python

# Copyright 2019 Google, LLC.
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

import sys

def create_cluster(project_id, region, cluster_name):
    # [START create_cluster]
    from google.cloud import dataproc_v1

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # region = 'YOUR_CLUSTER_REGION'
    # cluster_name = 'YOUR_CLUSTER_NAME'

    # Create client
    client = dataproc_v1.ClusterControllerClient({
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    # Create cluster config
    cluster = {
        'project_id': project,
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

    # Define a callback
    def callback(operation_future):
        result = operation_future.result()
        print(result)

    # Submit cluster creation request
    response = client.create_cluster(project_id, region, cluster)
    
    # Add callback to cluster creation request
    response.add_done_callback(callback)
    
    print(response.metadata())
    # [END create_cluster]


