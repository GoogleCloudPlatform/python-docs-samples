#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import aiplatform


def create_model_endpoint(project: str, region: str, model_endpoint_name: str) -> str:
    """Creates a model endpoint in AI Platform.

    Args:
        project: Google Cloud Project Id.
        region: Location for AI Platform resources.
        model_endpoint_name: AI Platform deployment endpoint name.

    Returns:
        The deployed model_endpoint_id.
    """
    client = aiplatform.gapic.EndpointServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.create_endpoint(
        parent=f"projects/{project}/locations/{region}",
        endpoint={"display_name": model_endpoint_name},
    )
    print(f"Creating model endpoint, operation: {response.operation.name}")
    model_endpoint = response.result()
    print(f"Model endpoint created\n{model_endpoint}")
    model_endpoint_id = model_endpoint.name.split("/")[-1]
    return model_endpoint_id


def deploy_model(
    project: str, region: str, model_path: str, model_name: str, model_endpoint_id: str
) -> str:
    """Deploys a model into an endpoint in AI Platform.

    Args:
        project: Google Cloud Project Id.
        region: Location for AI Platform resources.
        model_path: full model path.
        model_name: deployed model name.
        model_endpoint_id: deployment endpoint ID.

    Returns:
        The deployed_model_id.
    """
    client = aiplatform.gapic.EndpointServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    response = client.deploy_model(
        endpoint=client.endpoint_path(project, region, model_endpoint_id),
        deployed_model={
            "model": model_path,
            "display_name": model_name,
            "automatic_resources": {
                "min_replica_count": 1,
                "max_replica_count": 1,
            },
        },
        # key '0' assigns traffic for the newly deployed model
        # Traffic percentage values must add up to 100
        traffic_split={"0": 100},
    )
    print(f"Deploying model, operation: {response.operation.name}")
    deployed_model = response.result()
    print(f"Model deployed\n{deployed_model}")
    return deployed_model.deployed_model.id


def run(project: str, region: str, model_path: str, model_endpoint_name: str) -> None:
    """Creates an endpoint in AI Platform and deploys a model to it.

    Args:
        project: Google Cloud Project Id.
        region: Location for AI Platform resources.
        model_path: full model path.
        model_endpoint_name: deployment endpoint name.

    Returns:
        The deployed model_endpoint_id.
    """
    model_endpoint_id = create_model_endpoint(project, region, model_endpoint_name)
    deploy_model(project, region, model_path, model_endpoint_name, model_endpoint_id)
    return model_endpoint_id


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        required=True,
        help="Google Cloud Project Id",
    )
    parser.add_argument(
        "--region",
        required=True,
        help="Location for AI Platform resources",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Full model path",
    )
    parser.add_argument(
        "--model-endpoint-name",
        required=True,
        help="Deployment endpoint name",
    )
    args = parser.parse_args()

    run(args.project, args.region, args.model_path, args.model_endpoint_name)
