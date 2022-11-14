# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gke_list_cluster]
import argparse
import sys

from google.cloud import container_v1


def list_clusters(project_id: str, location: str) -> None:
    """List all the GKE clusters in the given GCP Project and Zone"""

    # Initialize the Cluster management client.
    client = container_v1.ClusterManagerClient()
    # Create a fully qualified location identifier of form `projects/{project_id}/location/{zone}'.
    cluster_location = client.common_location_path(project_id, location)
    # Create the request object with the location identifier.
    request = {"parent": cluster_location}
    list_response = client.list_clusters(request)

    print(
        f"There were {len(list_response.clusters)} clusters in {location} for project {project_id}."
    )
    for cluster in list_response.clusters:
        print(f"- {cluster.name}")


# [END gke_list_cluster]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("zone", help="GKE Cluster zone")
    args = parser.parse_args()

    if len(sys.argv) != 3:
        parser.print_usage()
        sys.exit(1)

    list_clusters(args.project_id, args.zone)
