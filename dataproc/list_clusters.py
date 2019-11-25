# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def list_clusters(project_id, region):
    """List the details of clusters in the region."""
    # [START dataproc_list_clusters]
    from google.cloud import dataproc_v1 as dataproc

    cluster_client = dataproc.ClusterControllerClient({
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    for cluster in cluster_client.list_clusters(project_id, region):
        print(('{} - {}'.format(cluster.cluster_name,
                                cluster.status.State.Name(
                                    cluster.status.state))))
    # [END dataproc_list_clusters]