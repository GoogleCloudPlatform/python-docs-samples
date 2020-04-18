#!/usr/bin/env python

# Copyright 2020 Google LLC
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

# This sample walks a user through creating a Cloud Dataproc cluster using
# the Python client library and a json configuration.

# [START dataproc_create_cluster]

import google.cloud.dataproc_v1beta2.proto.clusters_pb2 as clusters
import google.protobuf.json_format as json_format
from google.cloud import dataproc_v1beta2


def create_cluster(cluster_json_path, region):
    '''
    This function takes an external JSON with cluster
    configuration and creates the cluster.
    :param project_id: project id of the service account
    :param region: region where needs to be created
    :return: returns the cluster client instance
    '''
    cluster_client = dataproc_v1beta2.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    # The JOSN is created under the clusterconfig folder
    with open(cluster_json_path, 'r') as f:
        cluster_json = f.read()
        cluster_config = json_format.Parse(cluster_json, clusters.Cluster())

    project_id = cluster_config.project_id
    operation = cluster_client.create_cluster(project_id,
                                              region,
                                              cluster_config)
    result = operation.result()

    # Output a success message.
    print('Cluster created successfully : {}'.format(result.cluster_name))
    # [END dataproc_create_cluster]
