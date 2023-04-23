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

# [START gke_delete_cluster]
import argparse
import sys
from typing import Dict

import backoff
from google.cloud import container_v1


def on_success(details: Dict[str, str]) -> None:
    """
    A handler function to pass into the retry backoff algorithm as the function
    to be executed upon a successful attempt.

    Read the `Event handlers` section of the backoff python module at:
    https://pypi.org/project/backoff/
    """
    print("Successfully deleted cluster after {elapsed:0.1f} seconds".format(**details))


def on_failure(details: Dict[str, str]) -> None:
    """
    A handler function to pass into the retry backoff algorithm as the function
    to be executed upon a failed attempt.

    Read the `Event handlers` section of the backoff python module at:
    https://pypi.org/project/backoff/
    """
    print("Backing off {wait:0.1f} seconds after {tries} tries".format(**details))


@backoff.on_predicate(
    # the backoff algorithm to use. we use exponential backoff here
    backoff.expo,
    # the test function on the return value to determine if a retry is necessary
    lambda x: x != container_v1.Operation.Status.DONE,
    # maximum number of times to retry before giving up
    max_tries=20,
    # function to execute upon a failure and when a retry is scheduled
    on_backoff=on_failure,
    # function to execute upon a successful attempt and no more retries needed
    on_success=on_success,
)
def poll_for_op_status(
    client: container_v1.ClusterManagerClient, op_id: str
) -> container_v1.Operation.Status:
    """
    A simple retry function that fetches the operation and returns it's status.

    The function is annotated with the `backoff` python module to schedule this
    function based on a reasonable backoff algorithm
    """

    op = client.get_operation({"name": op_id})
    return op.status


def delete_cluster(project_id: str, location: str, cluster_name: str) -> None:
    """Delete an existing GKE cluster in the given GCP Project and Zone"""

    # Initialize the Cluster management client.
    client = container_v1.ClusterManagerClient()
    # Create a fully qualified location identifier of form `projects/{project_id}/location/{zone}'.
    cluster_location = client.common_location_path(project_id, location)
    cluster_name = f"{cluster_location}/clusters/{cluster_name}"
    # Create the request object with the location identifier.
    request = {"name": cluster_name}
    delete_response = client.delete_cluster(request)
    op_identifier = f"{cluster_location}/operations/{delete_response.name}"
    # poll for the operation status until the cluster is deleted
    poll_for_op_status(client, op_identifier)


# [END gke_delete_cluster]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("zone", help="GKE Cluster zone")
    parser.add_argument("cluster_name", help="Name to be given to the GKE Cluster")
    args = parser.parse_args()

    if len(sys.argv) != 4:
        parser.print_usage()
        sys.exit(1)

    delete_cluster(args.project_id, args.zone, args.cluster_name)
