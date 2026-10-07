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
listing templates.
"""


# [START parametermanager_list_param_templates]
def list_param_templates(project_id: str) -> None:
    """
    Lists all templates in the global location of the specified project using
    the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.

    Returns:
        None

    Example:
        list_param_templates(
            "my-project"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parent project in the global location.
    parent = client.common_location_path(project_id, "global")

    # List all templates in the parent project and location.
    for template in client.list_templates(parent=parent):
        print(f"Found template {template.name} with format {template.format_.name}")
    # [END parametermanager_list_param_templates]
