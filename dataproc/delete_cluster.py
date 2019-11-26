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

# [START_dataproc_delete_cluster]
from google.cloud import dataproc_v1 as dataproc


def delete_cluster(project_id, region, cluster_name):
    """Deletes a Cloud Dataproc cluster."""
    cluster_client = dataproc.ClusterControllerClient(client_options={
      'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    operation = cluster_client.delete_cluster(project_id, region, cluster_name)

    # Block the asynchronous delete_cluster call until deletion is finished.
    operation.result()

    # Output a success message
    print('Cluster deleted successfully: {}'.format(cluster_name))
    # [END_dataproc_delete_cluster]
