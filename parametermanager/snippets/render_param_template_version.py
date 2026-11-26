#!/usr/bin/env python

# Copyright 2026 Google LLC
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
rendering a template version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_render_param_template_version]
def render_param_template_version(
    project_id: str,
    template_id: str,
    version_id: str,
    parameter_id: str,
    parameter_version_id: str,
) -> parametermanager_v1.RenderTemplateVersionResponse:
    """
    Renders a version of an existing template in the global location of the
    specified project, resolving its placeholders with the values of a parameter
    version, using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.
        template_id (str): The ID of the template to be rendered.
        version_id (str): The ID of the template version to be rendered.
        parameter_id (str): The ID of the parameter whose version supplies the
        values.
        parameter_version_id (str): The ID of the parameter version that
        supplies the values.

    Returns:
        parametermanager_v1.RenderTemplateVersionResponse: An object representing the rendered
        template version.

    Example:
        render_param_template_version(
            "my-project",
            "my-template",
            "v1",
            "my-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the template version.
    name = client.template_version_path(project_id, "global", template_id, version_id)

    # Build the resource name of the parameter version that supplies the values.
    parameter_version = client.parameter_version_path(
        project_id, "global", parameter_id, parameter_version_id
    )

    # Define the request to render the template version.
    request = parametermanager_v1.RenderTemplateVersionRequest(
        name=name, parameter_version=parameter_version
    )

    # Render the template version.
    response = client.render_template_version(request=request)

    # Print the template payload and the rendered payload.
    print(f"Template payload: {response.payload.data.decode('utf-8')}")
    print(f"Rendered payload: {response.rendered_payload.decode('utf-8')}")
    # [END parametermanager_render_param_template_version]

    return response
