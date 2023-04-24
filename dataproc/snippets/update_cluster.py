#!/usr/bin/env python

# Copyright 2021 Google LLC
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

# This sample walks a user through updating the number of clusters using the Dataproc
# client library.

# Usage:
#  python update_cluster.py --project_id <PROJECT_ID> --region <REGION> --cluster_name <CLUSTER_NAME>

import sys

# [START dataproc_update_cluster]
from google.cloud import dataproc_v1 as dataproc


def update_cluster(project_id, region, cluster_name, new_num_instances):
    """This sample walks a user through updating a Cloud Dataproc cluster
    using the Python client library.

    Args:
        project_id (str): Project to use for creating resources.
        region (str): Region where the resources should live.
        cluster_name (str): Name to use for creating a cluster.
    """

    # Create a client with the endpoint set to the desired cluster region.
    client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )

    # Get cluster you wish to update.
    cluster = client.get_cluster(
        project_id=project_id, region=region, cluster_name=cluster_name
    )

    # Update number of clusters
    mask = {"paths": {"config.worker_config.num_instances": str(new_num_instances)}}

    # Update cluster config
    cluster.config.worker_config.num_instances = new_num_instances

    # Update cluster
    operation = client.update_cluster(
        project_id=project_id,
        region=region,
        cluster=cluster,
        cluster_name=cluster_name,
        update_mask=mask,
    )

    # Output a success message.
    updated_cluster = operation.result()
    print(f"Cluster was updated successfully: {updated_cluster.cluster_name}")


# [END dataproc_update_cluster]


if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit("python update_cluster.py project_id region cluster_name")

        project_id = sys.argv[1]
        region = sys.argv[2]
        cluster_name = sys.argv[3]
        new_num_instances = sys.argv[4]
        update_cluster(project_id, region, cluster_name)
