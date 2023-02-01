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

# [START cloudoptimization_long_timeout]

from google.cloud import optimization_v1
from google.cloud.optimization_v1.services import fleet_routing
from google.cloud.optimization_v1.services.fleet_routing import transports
from google.cloud.optimization_v1.services.fleet_routing.transports import (
    grpc as fleet_routing_grpc,
)

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'


def long_timeout(request_file_name: str, project_id: str) -> None:
    with open(request_file_name, "r") as f:
        fleet_routing_request = optimization_v1.OptimizeToursRequest.from_json(f.read())
        fleet_routing_request.parent = f"projects/{project_id}"

    # Create a channel to provide a connection to the Fleet Routing servers with
    # custom behavior. The `grpc.keepalive_time_ms` channel argument modifies
    # the channel behavior in order to send keep-alive pings every 5 minutes.
    channel = fleet_routing_grpc.FleetRoutingGrpcTransport.create_channel(
        options=[
            ("grpc.keepalive_time_ms", 500),
            ("grpc.max_send_message_length", -1),
            ("grpc.max_receive_message_length", -1),
        ],
    )
    # Keep-alive pings are sent on the transport. Create the transport using the
    # custom channel The transport is essentially a wrapper to the channel.
    transport = transports.FleetRoutingGrpcTransport(channel=channel)
    client = fleet_routing.client.FleetRoutingClient(transport=transport)
    fleet_routing_response = client.optimize_tours(fleet_routing_request)
    print(fleet_routing_response)


# [END cloudoptimization_long_timeout]
