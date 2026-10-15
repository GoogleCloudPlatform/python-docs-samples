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
quickstart with regional parameter manager templates.
"""


# [START parametermanager_regional_template_quickstart]
def regional_template_quickstart(
    project_id: str,
    location_id: str,
    template_id: str,
    parameter_id: str,
    version_id: str,
) -> None:
    """
    Creates a template, a parameter version and renders the template version.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are created.
        template_id (str): The ID to assign to the new template.
        parameter_id (str): The ID to assign to the new parameter.
        version_id (str): The ID used for both the template version and
        the parameter version.

    Returns:
        None

    Example:
        regional_template_quickstart(
            "my-project",
            "us-central1",
            "my-template",
            "my-parameter",
            "v1"
        )
    """
    # Import the necessary libraries.
    from google.cloud import parametermanager_v1
    import json

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parent project in the specified region.
    parent = client.common_location_path(project_id, location_id)

    # Create a template in JSON format.
    template = client.create_template(
        request=parametermanager_v1.CreateTemplateRequest(
            parent=parent,
            template_id=template_id,
            template=parametermanager_v1.Template(
                format_=parametermanager_v1.TemplateFormat.TEMPLATE_FORMAT_JSON
            ),
        )
    )
    print(f"Created regional template: {template.name}")

    # Create a template version with {{.variableName}} placeholders.
    template_payload = {"username": "{{.username}}", "host": "{{.host}}"}
    template_version = client.create_template_version(
        request=parametermanager_v1.CreateTemplateVersionRequest(
            parent=template.name,
            template_version_id=version_id,
            template_version=parametermanager_v1.TemplateVersion(
                payload=parametermanager_v1.TemplateVersionPayload(
                    data=json.dumps(template_payload).encode("utf-8")
                )
            ),
        )
    )
    print(f"Created regional template version: {template_version.name}")

    # Create a JSON parameter.
    parameter = client.create_parameter(
        request=parametermanager_v1.CreateParameterRequest(
            parent=parent,
            parameter_id=parameter_id,
            parameter=parametermanager_v1.Parameter(
                format_=parametermanager_v1.ParameterFormat.JSON
            ),
        )
    )
    print(f"Created regional parameter: {parameter.name}")

    # Create a parameter version that holds the values for the placeholders.
    values = {"username": "test-user", "host": "localhost"}
    parameter_version = client.create_parameter_version(
        request=parametermanager_v1.CreateParameterVersionRequest(
            parent=parameter.name,
            parameter_version_id=version_id,
            parameter_version=parametermanager_v1.ParameterVersion(
                payload=parametermanager_v1.ParameterVersionPayload(
                    data=json.dumps(values).encode("utf-8")
                )
            ),
        )
    )
    print(f"Created regional parameter version: {parameter_version.name}")

    # Render the template version with the parameter version's values.
    response = client.render_template_version(
        request=parametermanager_v1.RenderTemplateVersionRequest(
            name=template_version.name, parameter_version=parameter_version.name
        )
    )
    print(f"Rendered regional payload: {response.rendered_payload.decode('utf-8')}")
    # [END parametermanager_regional_template_quickstart]
