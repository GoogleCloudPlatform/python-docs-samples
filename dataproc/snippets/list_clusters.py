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

""" Sample command-line program to list Cloud Dataproc clusters in a region.

Example usage:
python list_clusters.py --project_id=my-project-id --region=global

"""
import argparse

from google.cloud import dataproc_v1


# [START dataproc_list_clusters]
def list_clusters(dataproc, project, region):
    """List the details of clusters in the region."""
    for cluster in dataproc.list_clusters(
        request={"project_id": project, "region": region}
    ):
        print(("{} - {}".format(cluster.cluster_name, cluster.status.state.name)))


# [END dataproc_list_clusters]


def main(project_id, region):

    if region == "global":
        # Use the default gRPC global endpoints.
        dataproc_cluster_client = dataproc_v1.ClusterControllerClient()
    else:
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        dataproc_cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
        )

    list_clusters(dataproc_cluster_client, project_id, region)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=(argparse.RawDescriptionHelpFormatter)
    )
    parser.add_argument("--project_id", help="Project ID to access.", required=True)
    parser.add_argument("--region", help="Region of clusters to list.", required=True)

    args = parser.parse_args()
    main(args.project_id, args.region)
