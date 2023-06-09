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

# [START cloudoptimization_async_api]

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import optimization_v1

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'
# request_file_name = 'YOUR_REQUEST_FILE_NAME'
# request_model_gcs_path = 'gs://YOUR_PROJECT/YOUR_BUCKET/YOUR_REQUEST_MODEL_PATH'
# model_solution_gcs_path = 'gs://YOUR_PROJECT/YOUR_BUCKET/YOUR_SOLUCTION_PATH'


def call_async_api(
    project_id: str, request_model_gcs_path: str, model_solution_gcs_path_prefix: str
) -> None:
    """Call the async api for fleet routing."""
    # Use the default credentials for the environment to authenticate the client.
    fleet_routing_client = optimization_v1.FleetRoutingClient()
    request_file_name = "resources/async_request.json"

    with open(request_file_name) as f:
        fleet_routing_request = optimization_v1.BatchOptimizeToursRequest.from_json(
            f.read()
        )
        fleet_routing_request.parent = f"projects/{project_id}"
        for idx, mc in enumerate(fleet_routing_request.model_configs):
            mc.input_config.gcs_source.uri = request_model_gcs_path
            model_solution_gcs_path = f"{model_solution_gcs_path_prefix}_{idx}"
            mc.output_config.gcs_destination.uri = model_solution_gcs_path

        # The timeout argument for the gRPC call is independent from the `timeout`
        # field in the request's OptimizeToursRequest message(s).
        operation = fleet_routing_client.batch_optimize_tours(fleet_routing_request)
        print(operation.operation.name)

        try:
            # Block to wait for the job to finish.
            result = operation.result()
            print(result)
            # Do you stuff.
        except GoogleAPICallError:
            print(operation.operation.error)


# [END cloudoptimization_async_api]
