#!/usr/bin/env python

# Copyright 2025 Google LLC
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
"""
command line application and sample code for
render the regional parameter version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_render_regional_param_version]
def render_regional_param_version(
    project_id: str, location_id: str, parameter_id: str, version_id: str
) -> parametermanager_v1.RenderParameterVersionResponse:
    """
    Retrieves and renders the details of a specific version of an
    existing parameter in the specified region of the specified project
    using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        location_id (str): The ID of the region where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which version details are to be rendered.
        version_id (str): The ID of the version to be rendered.

    Returns:
        parametermanager_v1.RenderParameterVersionResponse: An object
        representing the rendered parameter version.

    Example:
        render_regional_param_version(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter version.
    name = client.parameter_version_path(
        project_id, location_id, parameter_id, version_id
    )

    # Define the request to render the parameter version.
    request = parametermanager_v1.RenderParameterVersionRequest(name=name)

    # Get the rendered parameter version details.
    response = client.render_parameter_version(request=request)

    # Print the response payload.
    print(
        f"Rendered regional parameter version payload: "
        f"{response.rendered_payload.decode('utf-8')}"
    )
    # [END parametermanager_render_regional_param_version]

    return response
