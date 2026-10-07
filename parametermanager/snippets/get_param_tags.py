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
getting the tags of a parameter.
"""

from google.cloud import resourcemanager_v3


# [START parametermanager_get_param_tags]
def get_param_tags(
    project_id: str, parameter_id: str
) -> list[resourcemanager_v3.TagBinding]:
    """
    Gets the tags bound to an existing parameter in the global location of the
    specified project.
    Tags are input-only on the parameter itself, so they are read as
    tag bindings through the Resource Manager API.

    Args:
        project_id (str): The ID of the project.
        parameter_id (str): The ID of the parameter whose tags are retrieved.

    Returns:
        list[resourcemanager_v3.TagBinding]: The tag bindings of the parameter.

    Example:
        get_param_tags(
            "my-project",
            "my-parameter"
        )
    """
    # Import the necessary libraries.
    from google.cloud import parametermanager_v1
    from google.cloud import resourcemanager_v3

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Create the Resource Manager tag bindings client.
    resource_manager_client = resourcemanager_v3.TagBindingsClient()

    # Build the resource name of the parameter and get it. The parameter name
    # contains the project number, which the tag bindings parent requires.
    name = client.parameter_path(project_id, "global", parameter_id)
    parameter = client.get_parameter(request={"name": name})

    # List the tag bindings of the parameter.
    request = resourcemanager_v3.ListTagBindingsRequest(
        parent=f"//parametermanager.googleapis.com/{parameter.name}"
    )
    bindings = list(resource_manager_client.list_tag_bindings(request=request))

    # Print the tags of the parameter.
    for binding in bindings:
        print(f"Found parameter tag: {binding.tag_value}")
    # [END parametermanager_get_param_tags]

    return bindings
