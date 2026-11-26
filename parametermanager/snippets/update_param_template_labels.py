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
updating the labels of a template.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_update_param_template_labels]
def update_param_template_labels(
    project_id: str, template_id: str, key: str, value: str
) -> parametermanager_v1.Template:
    """
    Adds or updates a label on an existing template in the global location of
    the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.
        template_id (str): The ID of the template whose labels are to be
        updated.
        key (str): The label key.
        value (str): The label value.

    Returns:
        parametermanager_v1.Template: An object representing the updated template.

    Example:
        update_param_template_labels(
            "my-project",
            "my-template",
            "environment",
            "production"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    from google.protobuf import field_mask_pb2

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the template.
    name = client.template_path(project_id, "global", template_id)

    # Get the current template and set the label.
    template = client.get_template(request={"name": name})
    template.labels[key] = value

    # Define the update mask for the labels field.
    update_mask = field_mask_pb2.FieldMask(paths=["labels"])

    # Update the template.
    request = parametermanager_v1.UpdateTemplateRequest(
        template=template, update_mask=update_mask
    )
    client.update_template(request=request)

    # Get the updated template.
    response = client.get_template(request={"name": name})

    # Print the updated labels.
    print(f"Updated template {response.name} with labels {dict(response.labels)}")
    # [END parametermanager_update_param_template_labels]

    return response
