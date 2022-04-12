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

# [START cloudoptimization_sync_api]

from google.cloud import optimization_v1

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'


def call_sync_api(project_id: str) -> None:
    """Call the sync api for fleet routing."""
    # Use the default credentials for the environment.
    # Change the file name to your request file.
    request_file_name = "resources/sync_request.json"
    fleet_routing_client = optimization_v1.FleetRoutingClient()

    with open(request_file_name, "r") as f:
        # The request must include the `parent` field with the value set to
        # 'projects/{YOUR_GCP_PROJECT_ID}'.
        fleet_routing_request = optimization_v1.OptimizeToursRequest.from_json(f.read())
        fleet_routing_request.parent = f"projects/{project_id}"
        # Send the request and print the response.
        # Fleet Routing will return a response by the earliest of the `timeout`
        # field in the request payload and the gRPC timeout specified below.
        fleet_routing_response = fleet_routing_client.optimize_tours(
            fleet_routing_request, timeout=100
        )
        print(fleet_routing_response)
        # If you want to format the response to JSON, you can do the following:
        # from google.protobuf.json_format import MessageToJson
        # json_obj = MessageToJson(fleet_routing_response._pb)


# [END cloudoptimization_sync_api]
