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
creating a new template version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_param_template_version]
def create_param_template_version(
    project_id: str, template_id: str, version_id: str
) -> parametermanager_v1.TemplateVersion:
    """
    Creates a new template version with placeholders in its payload.

    Args:
        project_id (str): The ID of the project.
        template_id (str): The ID of the template for which the version is to be
        created.
        version_id (str): The ID of the template version to be created.

    Returns:
        parametermanager_v1.TemplateVersion: An object representing the newly created
        template version.

    Example:
        create_param_template_version(
            "my-project",
            "my-template",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    import json

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the template.
    parent = client.template_path(project_id, "global", template_id)

    # Define the template payload.
    payload_data = {"username": "{{.username}}", "host": "{{.host}}"}
    payload = parametermanager_v1.TemplateVersionPayload(
        data=json.dumps(payload_data).encode("utf-8")
    )

    # Define the template version creation request.
    request = parametermanager_v1.CreateTemplateVersionRequest(
        parent=parent,
        template_version_id=version_id,
        template_version=parametermanager_v1.TemplateVersion(payload=payload),
    )

    # Create the template version.
    response = client.create_template_version(request=request)

    # Print the newly created template version name.
    print(f"Created template version: {response.name}")
    # [END parametermanager_create_param_template_version]

    return response
